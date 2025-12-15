# Marcos Vinicius Brito de Araujo - 202404940009
# Maurício Aires Pinheiro - 202404940003

import sys
sys.stdout.reconfigure(encoding='utf-8')

class NodeAVL:
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None
        self.altura = 1

class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def _altura(self, node):
        return node.altura if node else 0

    def _obter_balanco(self, node):
        return self._altura(node.esquerda) - self._altura(node.direita) if node else 0

    def _rotacionar_direita(self, node_desbalanceado):
        pivo = node_desbalanceado.esquerda
        auxiliar = pivo.direita

        pivo.direita = node_desbalanceado
        node_desbalanceado.esquerda = auxiliar

        node_desbalanceado.altura = 1 + max(self._altura(node_desbalanceado.esquerda), self._altura(node_desbalanceado.direita))
        pivo.altura = 1 + max(self._altura(pivo.esquerda), self._altura(pivo.direita))

        return pivo

    def _rotacionar_esquerda(self, node_desbalanceado):
        pivo = node_desbalanceado.direita
        auxiliar = pivo.esquerda

        pivo.esquerda = node_desbalanceado
        node_desbalanceado.direita = auxiliar

        node_desbalanceado.altura = 1 + max(self._altura(node_desbalanceado.esquerda), self._altura(node_desbalanceado.direita))
        pivo.altura = 1 + max(self._altura(pivo.esquerda), self._altura(pivo.direita))

        return pivo

    def inserir(self, chave):
        self.raiz = self._inserir_recursivo(self.raiz, chave)

    def _inserir_recursivo(self, node_atual, chave):
        if not node_atual:
            return NodeAVL(chave)
        
        if chave < node_atual.chave:
            node_atual.esquerda = self._inserir_recursivo(node_atual.esquerda, chave)

        elif chave > node_atual.chave:
            node_atual.direita = self._inserir_recursivo(node_atual.direita, chave)

        else:
            return node_atual # Chaves duplicadas não são inseridas

        node_atual.altura = 1 + max(self._altura(node_atual.esquerda), self._altura(node_atual.direita))
        balanco = self._obter_balanco(node_atual)

        # Balanceamento
        if balanco > 1 and chave < node_atual.esquerda.chave: # Pra esquerda
            return self._rotacionar_direita(node_atual)

        if balanco < -1 and chave > node_atual.direita.chave: # Pra direita
            return self._rotacionar_esquerda(node_atual)

        if balanco > 1 and chave > node_atual.esquerda.chave: # Dupla pra direita
            node_atual.esquerda = self._rotacionar_esquerda(node_atual.esquerda)
            return self._rotacionar_direita(node_atual)

        if balanco < -1 and chave < node_atual.direita.chave: # Dupla pra esquerda
            node_atual.direita = self._rotacionar_direita(node_atual.direita)
            return self._rotacionar_esquerda(node_atual)

        return node_atual

    def remover(self, chave):
        self.raiz = self._remover_recursivo(self.raiz, chave)

    def _remover_recursivo(self, node_atual, chave):
        if not node_atual:
            return node_atual

        if chave < node_atual.chave:
            node_atual.esquerda = self._remover_recursivo(node_atual.esquerda, chave)

        elif chave > node_atual.chave:
            node_atual.direita = self._remover_recursivo(node_atual.direita, chave)

        else:
            if not node_atual.esquerda:
                return node_atual.direita
            
            elif not node_atual.direita:
                return node_atual.esquerda
            
            temp = self._obter_minimo(node_atual.direita)
            node_atual.chave = temp.chave
            node_atual.direita = self._remover_recursivo(node_atual.direita, temp.chave)

        if not node_atual:
            return node_atual

        node_atual.altura = 1 + max(self._altura(node_atual.esquerda), self._altura(node_atual.direita))
        balanco = self._obter_balanco(node_atual)

        # Balanceamento
        if balanco > 1 and self._obter_balanco(node_atual.esquerda) >= 0: # Pra direita
            return self._rotacionar_direita(node_atual)
        
        if balanco > 1 and self._obter_balanco(node_atual.esquerda) < 0: # Dupla pra direita
            node_atual.esquerda = self._rotacionar_esquerda(node_atual.esquerda)
            return self._rotacionar_direita(node_atual)
        
        if balanco < -1 and self._obter_balanco(node_atual.direita) <= 0: # Pra esquerda
            return self._rotacionar_esquerda(node_atual)
        
        if balanco < -1 and self._obter_balanco(node_atual.direita) > 0: # Dupla pra esquerda
            node_atual.direita = self._rotacionar_direita(node_atual.direita)
            return self._rotacionar_esquerda(node_atual)

        return node_atual

    def _obter_minimo(self, node):
        atual = node
        while atual.esquerda:
            atual = atual.esquerda
        return atual

    def pesquisar(self, chave):
        self._pesquisar_recursivo(self.raiz, chave)

    def _pesquisar_recursivo(self, node, chave):
        if not node:
            print(f'Não achou a chave {chave}')
            return None
        
        elif node.chave == chave:
            print(f'Achou a chave {chave}')
            return node

        if chave < node.chave:
            self._pesquisar_recursivo(node.esquerda, chave)

        else:
            self._pesquisar_recursivo(node.direita, chave)

    def mostrar(self):
        if not self.raiz:
            print("Árvore Vazia")
            return

        self._imprimir_arvore(self.raiz, "", True)

    def _imprimir_arvore(self, node, prefixo="", cauda=True):
        if node.direita:
            prefixo_novo = prefixo + ("│   " if cauda else "    ")
            self._imprimir_arvore(node.direita, prefixo_novo, False)
        
        print(prefixo + ("└── " if cauda else "┌── ") + str(node.chave))
        
        if node.esquerda:
            prefixo_novo = prefixo + ("    " if cauda else "│   ")
            self._imprimir_arvore(node.esquerda, prefixo_novo, True)


arvore_avl = ArvoreAVL()
valores = [50, 25, 75, 15, 35, 60, 120, 10, 68, 90, 125, 83, 100, 25, 3, 7, 12, 84, 302, 1, 123, 101]

for valor in valores:
    arvore_avl.inserir(valor)

chave = 83
print(f"Pesquisando chave {chave}:")
arvore_avl.pesquisar(chave)

arvore_avl.mostrar()