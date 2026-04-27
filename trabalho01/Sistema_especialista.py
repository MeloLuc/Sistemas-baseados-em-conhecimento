# ============================================================
#  Sistema Especialista - Diagnóstico de Hardware de PC
# ============================================================

# ============================================================
# PARTE 1 - BASE DE CONHECIMENTO
# ============================================================

# Representa uma regra lógica única do domínio especialista.
# Cada regra possui uma "condição" (teste lógico) e uma "conclusão" (diagnóstico).
class Rule:
    def __init__(self, condition, conclusion):
        self.condition = condition
        self.conclusion = conclusion

    def evaluate(self, data):
        if self.condition(data):
            return self.conclusion
        return None

# Funciona como o "cérebro" ou banco de dados do sistema.
# Responsável por armazenar todas as regras e testar os dados do usuário contra elas.
class KnowledgeBase:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def get_conclusion(self, data):
        conclusoes_encontradas = []
        for rule in self.rules:
            resultado = rule.evaluate(data)
            if resultado:
                conclusoes_encontradas.append(resultado)
        return conclusoes_encontradas

# ============================================================
# PARTE 2 - MECANISMO DE INFERÊNCIA
# ============================================================

# É o motor lógico que executa o Encadeamento para Frente (Forward Chaining).
# Ele recebe os sintomas do usuário e extrai as deduções da Base de Conhecimento.
class InferenceEngine:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def infer(self, data):
        conclusoes = self.knowledge_base.get_conclusion(data)

        # Se nenhuma regra for ativada, retorna um diagnóstico padrão de segurança
        if not conclusoes:
            return ["Sintomas inconclusivos. Recomenda-se análise técnica em bancada."]

        return conclusoes

# ============================================================
# PARTE 3 - INTERFACE COM O USUÁRIO
# ============================================================

# Gerencia toda a experiência e interação com quem está usando o sistema.
# Responsável por imprimir textos formatados, coletar as respostas e exibir resultados.
class UserInterface:
    def __init__(self, inference_engine):
        self.inference_engine = inference_engine

    def _linha(self, caractere="=", tamanho=70):
        print(caractere * tamanho)

    def _cabecalho(self):
        self._linha()
        print("   SISTEMA ESPECIALISTA - DIAGNÓSTICO DE PC")
        self._linha()
        print("  Responda às perguntas com 's' (sim) ou 'n' (não).")
        print("  O sistema investigará o problema por camadas de hardware.\n")

    def _perguntar(self, pergunta):
        resposta = input(pergunta).strip().lower()
        return resposta in ['s', 'sim']

    # Implementa a árvore de decisão interativa.
    # As perguntas se adaptam (aninhadas) dependendo das respostas anteriores do usuário.
    def get_user_input(self):
        print("\n  Iniciando diagnóstico...")
        self._linha("-", 70)
        
        d = {} 
        
        # --- ÁRVORE DE DECISÃO PROFUNDA ---
        
        # CAMADA 1: ENERGIA
        d['nao_liga'] = self._perguntar("  1. O PC não dá nenhum sinal de vida ao apertar o botão? (s/n): ")
        if d['nao_liga']:
            d['sem_energia'] = self._perguntar("     -> Nenhuma luz na placa acende ou cooler tenta girar? (s/n): ")
            return d # Encerra a coleta, problema elétrico grave

        # CAMADA 2: POST / VÍDEO
        d['sem_video'] = self._perguntar("  2. O PC liga (coolers giram), mas NÃO dá imagem na tela? (s/n): ")
        if d['sem_video']:
            d['com_bipes'] = self._perguntar("     -> A placa-mãe emite bipes sonoros? (s/n): ")
            if d['com_bipes']:
                d['bipes_memoria'] = self._perguntar("        -> São bipes longos e repetitivos? (s/n): ")
            return d # Encerra a coleta, problema de boot

        # CAMADA 3: ESTABILIDADE E SISTEMA OPERACIONAL
        d['instavel'] = self._perguntar("  3. O Windows inicia, mas o sistema está instável (desliga ou trava)? (s/n): ")
        if d['instavel']:
            d['tela_azul'] = self._perguntar("     -> Ocorre a Tela Azul da Morte (BSOD)? (s/n): ")
            if d['tela_azul']:
                d['bsod_frequente'] = self._perguntar("        -> Acontece logo ao ligar o PC (durante o boot)? (s/n): ")
            else:
                d['desliga_pesado'] = self._perguntar("     -> Ele desliga tudo repentinamente quando você joga ou abre algo pesado? (s/n): ")
            return d # Encerra a coleta, problema de estabilidade

        # CAMADA 4: GRÁFICOS E DESEMPENHO
        d['artefatos'] = self._perguntar("  4. A imagem apresenta riscos, manchas ou quadrados coloridos piscando? (s/n): ")
        if not d['artefatos']:
            d['lento'] = self._perguntar("  5. O sistema está extremamente lento até para tarefas básicas? (s/n): ")
            if d['lento']:
                d['disco_cheio'] = self._perguntar("     -> O uso de disco ou CPU bate 100% no gerenciador de tarefas? (s/n): ")
        
        return d

    def display_result(self, conclusions):
        self._linha("-", 70)
        print("  DIAGNÓSTICO TÉCNICO")
        self._linha("-", 70)

        if len(conclusions) == 1 and "inconclusivos" in conclusions[0]:
            print(f"\n  [?] {conclusions[0]}\n")
        else:
            print(f"\n  Foi encontrado {len(conclusions)} possível(is) problema(s):\n")
            for diag in conclusions:
                print(f"   [!] {diag}")
            print("\n  Recomenda-se realizar backup dos dados se o sistema iniciar.\n")

        self._linha()

    # Ponto central que orquestra a execução da interface em um loop contínuo.
    def run(self):
        self._cabecalho()

        while True:
            dados_sintomas = self.get_user_input()
            conclusoes = self.inference_engine.infer(dados_sintomas)
            self.display_result(conclusoes)

            repetir = input("  Deseja diagnosticar outro computador? (s/n): ").strip().lower()
            if repetir not in ['s', 'sim']:
                print("\n  Sistema encerrado.\n")
                break
            print()

# ============================================================
# CONFIGURAÇÃO E EXECUÇÃO
# ============================================================

# Este bloco só roda se o arquivo for executado diretamente.
# É aqui que o "conhecimento" do especialista é cadastrado no sistema.
if __name__ == "__main__":
    kb = KnowledgeBase()

    # --- REGRAS DA CAMADA DE ENERGIA ---
    kb.add_rule(Rule(
        lambda d: d.get('nao_liga') and d.get('sem_energia'), 
        "Falha de Energia: Fonte de alimentação queimada, chave no '0' ou cabo de força defeituoso."
    ))
    kb.add_rule(Rule(
        lambda d: d.get('nao_liga') and d.get('sem_energia') is False, 
        "Curto-circuito: Placa-mãe em proteção contra curto ou botão Power do gabinete danificado."
    ))

    # --- REGRAS DA CAMADA DE POST/VÍDEO ---
    kb.add_rule(Rule(
        lambda d: d.get('sem_video') and d.get('com_bipes') and d.get('bipes_memoria'), 
        "Erro de Memória: Remova os pentes de RAM, limpe os contatos com borracha e recoloque."
    ))
    kb.add_rule(Rule(
        lambda d: d.get('sem_video') and d.get('com_bipes') and d.get('bipes_memoria') is False, 
        "Erro de GPU: Placa de vídeo mal encaixada ou com defeito no chip gráfico."
    ))
    kb.add_rule(Rule(
        lambda d: d.get('sem_video') and d.get('com_bipes') is False, 
        "Falha de BIOS/CPU: BIOS corrompida ou processador não está sendo reconhecido."
    ))

    # --- REGRAS DA CAMADA DE ESTABILIDADE ---
    kb.add_rule(Rule(
        lambda d: d.get('instavel') and d.get('tela_azul') and d.get('bsod_frequente'), 
        "Sistema Corrompido: Arquivos do Windows corrompidos ou falha crítica em um driver de boot."
    ))
    kb.add_rule(Rule(
        lambda d: d.get('instavel') and d.get('tela_azul') and d.get('bsod_frequente') is False, 
        "Falha de Hardware/RAM: Pentes de memória defeituosos causando Tela Azul aleatória."
    ))
    kb.add_rule(Rule(
        lambda d: d.get('instavel') and d.get('tela_azul') is False and d.get('desliga_pesado'), 
        "Superaquecimento/Fonte: A fonte não está aguentando a carga ou o processador está superaquecendo."
    ))

    # --- REGRAS DA CAMADA DE GRÁFICOS/DESEMPENHO ---
    kb.add_rule(Rule(
        lambda d: d.get('artefatos'), 
        "Artefatos de Vídeo: Solda BGA da Placa de Vídeo falhando ou cabo HDMI/DisplayPort danificado."
    ))
    kb.add_rule(Rule(
        lambda d: d.get('lento') and d.get('disco_cheio'), 
        "Gargalo de I/O: Seu HD mecânico pode estar morrendo ou há malware consumindo recursos. Considere um SSD."
    ))

    # Instancia as engrenagens principais e inicia a interface
    engine = InferenceEngine(kb)
    ui = UserInterface(engine)
    ui.run()