#Sistema de Diagnóstico abordando temas exemplificados até o 5 capítulo do livro: A Guide to Expert Systems.
#Descrição: Programa desenvolvido para saber qual abordagem de solução é mais adequada: algorítmo ou heuristica.
#Disciplina: Sistema baseado em conhecimento
#Aluno: Lucas de Melo Monteiro Peixoto
#Data: 24/03/2026

class SistemaEspecialista:
    def __init__(self):
        # Conjunto de regras no formato "Se (condições) Então (conclusão)"
        self.regras = [
            {
                "se": ["busca_exaustiva_impossivel", "solucao_aproximada_aceitavel"],
                "entao": "abordagem_recomendada_heuristica"
            },
            {
                "se": ["garantia_solucao_otima_necessaria", "espaco_busca_pequeno"],
                "entao": "abordagem_recomendada_algoritmo_exato"
            },
            {
                "se": ["tempo_processamento_critico"],
                "entao": "solucao_aproximada_aceitavel"
            },
            {
                "se": ["muitas_variaveis_combinatorias"],
                "entao": "busca_exaustiva_impossivel"
            }
        ]
        
        # (Fatos conhecidos)
        self.fatos = set()

    def adicionar_fato(self, fato):
        self.fatos.add(fato)
        print(f"Fato adicionado: {fato}")

    def motor_de_inferencia(self):
        """
        (Forward Chaining)
        Avalia as regras iterativamente até que nenhum fato novo seja descoberto.
        """
        novos_fatos_descobertos = True

        while novos_fatos_descobertos:
            novos_fatos_descobertos = False
            
            for regra in self.regras:
                conclusao = regra["entao"]
                condicoes = regra["se"]

                # Se a conclusão já é um fato conhecido, pula para a próxima regra
                if conclusao in self.fatos:
                    continue

                # Verifica se todas as condições da regra estão presentes nos fatos atuais
                todas_condicoes_satisfeitas = all(condicao in self.fatos for condicao in condicoes)

                if todas_condicoes_satisfeitas:
                    print(f"Como temos {condicoes}, então deduzimos: {conclusao}")
                    self.fatos.add(conclusao)
                    novos_fatos_descobertos = True
                    

    def obter_diagnostico(self):
        """Filtra a memória de trabalho para entregar a recomendação final."""
        recomendacoes = [fato for fato in self.fatos if fato.startswith("abordagem_recomendada")]
        return recomendacoes if recomendacoes else ["Não foi possível chegar a uma conclusão."]
    


# Testando o sistema
sistema = SistemaEspecialista()

sistema.adicionar_fato("muitas_variaveis_combinatorias")
sistema.adicionar_fato("tempo_processamento_critico")
sistema.adicionar_fato("garantia_solucao_otima_necessaria")

# Executamos o motor de inferência
sistema.motor_de_inferencia()

# Verificamos a conclusão
diagnostico = sistema.obter_diagnostico()
print("\nDiagnóstico Final:")
for d in diagnostico:
    print(f"=> {d}")