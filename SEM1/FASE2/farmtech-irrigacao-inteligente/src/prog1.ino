/*
 * FarmTech Solutions - Sistema de Irrigacao Inteligente
 * Cultura: Tomate
 * 
 * Sensores simulados:
 *   - 3 Push Buttons (TOGGLE) -> Nitrogenio (N), Fosforo (P), Potassio (K)
 *   - LDR (Light Dependent Resistor) -> pH do solo
 *   - DHT22 -> Umidade do solo
 *   - Relay -> Bomba d'agua
 *   - LED Verde -> Indicador irrigacao ativa
 *   - LED Vermelho -> Alerta critico
 * 
 * Parametros ideais para Tomate:
 *   - pH: 5.5 a 7.0
 *   - Umidade: 60% a 80%
 *   - NPK: pelo menos 2 de 3 nutrientes presentes
 * 
 * Logica de irrigacao:
 *   A bomba liga quando:
 *     1. Umidade < 60% (solo seco)
 *     2. pH entre 5.5 e 7.0 (faixa aceitavel)
 *     3. Pelo menos 2 de 3 nutrientes (N, P, K) presentes
 *   
 *   A bomba NAO liga quando:
 *     - Umidade >= 80% (solo encharcado)
 *     - pH fora da faixa (precisa correcao do solo)
 *     - Menos de 2 nutrientes presentes
 *     - Previsao de chuva ativa (dado manual via Serial)
 */

#include "DHT.h"

// ===================== PINOS =====================
#define PIN_BTN_N     4
#define PIN_BTN_P     5
#define PIN_BTN_K    18

#define PIN_LDR      34
#define PIN_DHT      23

#define PIN_RELAY    26
#define PIN_LED_OK   27
#define PIN_LED_WARN 14

// ===================== CONSTANTES =====================
#define DHTTYPE DHT22

#define PH_MIN         5.5
#define PH_MAX         7.0
#define UMIDADE_MIN    60.0
#define UMIDADE_MAX    80.0

#define LDR_MIN  0
#define LDR_MAX  4095
#define PH_SCALE_MIN  0.0
#define PH_SCALE_MAX  14.0

#define INTERVALO_LEITURA 2000
#define DEBOUNCE_MS       200

// ===================== OBJETOS =====================
DHT dht(PIN_DHT, DHTTYPE);

// ===================== VARIAVEIS =====================
bool nitrogenio = false;
bool fosforo    = false;
bool potassio   = false;

bool lastBtnN = HIGH;
bool lastBtnP = HIGH;
bool lastBtnK = HIGH;

unsigned long lastDebounceN = 0;
unsigned long lastDebounceP = 0;
unsigned long lastDebounceK = 0;

float phSolo    = 7.0;
float umidade   = 0.0;
bool bombaLigada = false;
bool previsaoChuva = false;

unsigned long ultimaLeitura = 0;

// ===================== SETUP =====================
void setup() {
  Serial.begin(115200);
  Serial.println("===========================================");
  Serial.println("  FarmTech Solutions - Irrigacao Inteligente");
  Serial.println("  Cultura: Tomate");
  Serial.println("===========================================");
  Serial.println();
  Serial.println("Comandos via Serial:");
  Serial.println("  'C' -> Ativar previsao de chuva");
  Serial.println("  'S' -> Desativar previsao de chuva (sol)");
  Serial.println();
  Serial.println("Botoes NPK: clique para alternar ON/OFF");
  Serial.println();

  pinMode(PIN_BTN_N, INPUT_PULLUP);
  pinMode(PIN_BTN_P, INPUT_PULLUP);
  pinMode(PIN_BTN_K, INPUT_PULLUP);
  pinMode(PIN_LDR, INPUT);
  pinMode(PIN_RELAY, OUTPUT);
  pinMode(PIN_LED_OK, OUTPUT);
  pinMode(PIN_LED_WARN, OUTPUT);

  digitalWrite(PIN_RELAY, LOW);
  digitalWrite(PIN_LED_OK, LOW);
  digitalWrite(PIN_LED_WARN, LOW);

  dht.begin();
}

// ===================== FUNCOES AUXILIARES =====================

void verificarToggleBotoes() {
  unsigned long agora = millis();
  bool btnN = digitalRead(PIN_BTN_N);
  bool btnP = digitalRead(PIN_BTN_P);
  bool btnK = digitalRead(PIN_BTN_K);

  if (btnN == LOW && lastBtnN == HIGH && (agora - lastDebounceN > DEBOUNCE_MS)) {
    nitrogenio = !nitrogenio;
    lastDebounceN = agora;
    Serial.print(">> Nitrogenio (N): ");
    Serial.println(nitrogenio ? "ATIVADO" : "DESATIVADO");
  }
  lastBtnN = btnN;

  if (btnP == LOW && lastBtnP == HIGH && (agora - lastDebounceP > DEBOUNCE_MS)) {
    fosforo = !fosforo;
    lastDebounceP = agora;
    Serial.print(">> Fosforo (P): ");
    Serial.println(fosforo ? "ATIVADO" : "DESATIVADO");
  }
  lastBtnP = btnP;

  if (btnK == LOW && lastBtnK == HIGH && (agora - lastDebounceK > DEBOUNCE_MS)) {
    potassio = !potassio;
    lastDebounceK = agora;
    Serial.print(">> Potassio (K): ");
    Serial.println(potassio ? "ATIVADO" : "DESATIVADO");
  }
  lastBtnK = btnK;
}

float lerPH() {
  int ldrRaw = analogRead(PIN_LDR);
  return mapFloat(ldrRaw, LDR_MIN, LDR_MAX, PH_SCALE_MIN, PH_SCALE_MAX);
}

float mapFloat(float x, float inMin, float inMax, float outMin, float outMax) {
  return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
}

float lerUmidade() {
  float h = dht.readHumidity();
  if (isnan(h)) {
    Serial.println("[ERRO] Falha ao ler DHT22!");
    return -1;
  }
  return h;
}

void verificarSerial() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 'C' || cmd == 'c') {
      previsaoChuva = true;
      Serial.println(">> Previsao de CHUVA ativada!");
    } else if (cmd == 'S' || cmd == 's') {
      previsaoChuva = false;
      Serial.println(">> Previsao de SOL ativada!");
    }
  }
}

int contarNutrientes() {
  int count = 0;
  if (nitrogenio) count++;
  if (fosforo) count++;
  if (potassio) count++;
  return count;
}

bool decidirIrrigacao(float umid, float ph, int numNutrientes) {
  if (previsaoChuva) return false;
  if (umid >= UMIDADE_MAX) return false;
  if (ph < PH_MIN || ph > PH_MAX) return false;
  if (numNutrientes < 2) return false;
  if (umid < UMIDADE_MIN) return true;
  return false;
}

void controlarAtuadores(bool irrigar, float ph, int numNutrientes) {
  if (irrigar) {
    digitalWrite(PIN_RELAY, HIGH);
    digitalWrite(PIN_LED_OK, HIGH);
    bombaLigada = true;
  } else {
    digitalWrite(PIN_RELAY, LOW);
    digitalWrite(PIN_LED_OK, LOW);
    bombaLigada = false;
  }
  bool alerta = (ph < PH_MIN || ph > PH_MAX) || (numNutrientes < 2);
  if (previsaoChuva) alerta = false;
  digitalWrite(PIN_LED_WARN, alerta ? HIGH : LOW);
}

void imprimirStatus(float umid, float ph, int numNutrientes) {
  Serial.println("-------------------------------------------");
  Serial.println("         LEITURA DOS SENSORES              ");
  Serial.println("-------------------------------------------");
  Serial.print("  Nitrogenio (N): ");
  Serial.println(nitrogenio ? "PRESENTE [ON]" : "AUSENTE  [OFF]");
  Serial.print("  Fosforo    (P): ");
  Serial.println(fosforo ? "PRESENTE [ON]" : "AUSENTE  [OFF]");
  Serial.print("  Potassio   (K): ");
  Serial.println(potassio ? "PRESENTE [ON]" : "AUSENTE  [OFF]");
  Serial.print("  Nutrientes OK:  ");
  Serial.print(numNutrientes);
  Serial.println("/3");
  Serial.print("  pH do Solo:     ");
  Serial.print(ph, 1);
  Serial.print(" (ideal: ");
  Serial.print(PH_MIN, 1);
  Serial.print(" - ");
  Serial.print(PH_MAX, 1);
  Serial.println(")");
  Serial.print("  Umidade Solo:   ");
  Serial.print(umid, 1);
  Serial.print("% (ideal: ");
  Serial.print(UMIDADE_MIN, 0);
  Serial.print("% - ");
  Serial.print(UMIDADE_MAX, 0);
  Serial.println("%)");
  if (previsaoChuva) {
    Serial.println("  Previsao:       CHUVA PREVISTA");
  }
  Serial.println("-------------------------------------------");
  Serial.print("  >> BOMBA D'AGUA: ");
  Serial.println(bombaLigada ? "*** LIGADA ***" : "DESLIGADA");
  if (ph < PH_MIN || ph > PH_MAX) {
    Serial.println("  ! ALERTA: pH fora da faixa! Corrigir solo.");
  }
  if (numNutrientes < 2) {
    Serial.println("  ! ALERTA: Nutrientes insuficientes!");
  }
  if (previsaoChuva) {
    Serial.println("  i Irrigacao suspensa: chuva prevista.");
  }
  Serial.println("-------------------------------------------");
  Serial.println();
}

// ===================== LOOP PRINCIPAL =====================
void loop() {
  verificarSerial();
  verificarToggleBotoes();

  unsigned long agora = millis();
  if (agora - ultimaLeitura >= INTERVALO_LEITURA) {
    ultimaLeitura = agora;
    phSolo = lerPH();
    umidade = lerUmidade();
    if (umidade < 0) return;
    int numNutrientes = contarNutrientes();
    bool irrigar = decidirIrrigacao(umidade, phSolo, numNutrientes);
    controlarAtuadores(irrigar, phSolo, numNutrientes);
    imprimirStatus(umidade, phSolo, numNutrientes);
  }
}