# Marcos Vinicius Brito de Araujo - 202404940009
# Maurício Aires Pinheiro - 202404940003

import sys
sys.stdout.reconfigure(encoding='utf-8')

class NodeRN:
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None
        self.pai = None
        self.cor = 1 #1 = Vermelho, 0 = Preto

class ArvoreRubroNegra:
    def __init__(self):
        self.NIL = NodeRN(None)
        self.NIL.cor = 0
        self.raiz = self.NIL

    def _rotacionar_esquerda(self, node_desbalanceado):
        pivo = node_desbalanceado.direita
        node_desbalanceado.direita = pivo.esquerda
        if pivo.esquerda != self.NIL:
            pivo.esquerda.pai = node_desbalanceado

        pivo.pai = node_desbalanceado.pai
        if node_desbalanceado.pai == None:
            self.raiz = pivo

        elif node_desbalanceado == node_desbalanceado.pai.esquerda:
            node_desbalanceado.pai.esquerda = pivo

        else:
            node_desbalanceado.pai.direita = pivo

        pivo.esquerda = node_desbalanceado
        node_desbalanceado.pai = pivo

    def _rotacionar_direita(self, node_desbalanceado):
        pivo = node_desbalanceado.esquerda
        node_desbalanceado.esquerda = pivo.direita
        if pivo.direita != self.NIL:
            pivo.direita.pai = node_desbalanceado

        pivo.pai = node_desbalanceado.pai
        if node_desbalanceado.pai == None:
            self.raiz = pivo

        elif node_desbalanceado == node_desbalanceado.pai.direita:
            node_desbalanceado.pai.direita = pivo

        else:
            node_desbalanceado.pai.esquerda = pivo

        pivo.direita = node_desbalanceado
        node_desbalanceado.pai = pivo

    def inserir(self, chave):
        novo_node = NodeRN(chave)
        novo_node.esquerda = self.NIL
        novo_node.direita = self.NIL
        
        pai_aux = None
        atual = self.raiz

        while atual != self.NIL:
            pai_aux = atual
            if novo_node.chave < atual.chave:
                atual = atual.esquerda
            elif novo_node.chave == atual.chave:
                print(f"Chave {chave} já existe na árvore.")
                return
            else:
                atual = atual.direita

        novo_node.pai = pai_aux
        if pai_aux == None:
            self.raiz = novo_node

        elif novo_node.chave < pai_aux.chave:
            pai_aux.esquerda = novo_node

        else:
            pai_aux.direita = novo_node

        if novo_node.pai == None:
            novo_node.cor = 0
            return

        if novo_node.pai.pai == None:
            return

        self._ajustar_insercao(novo_node)

    def _ajustar_insercao(self, node_inserido):
        while node_inserido.pai.cor == 1:
            if node_inserido.pai == node_inserido.pai.pai.direita:
                tio = node_inserido.pai.pai.esquerda
                if tio.cor == 1:
                    tio.cor = 0
                    node_inserido.pai.cor = 0
                    node_inserido.pai.pai.cor = 1
                    node_inserido = node_inserido.pai.pai

                else:
                    if node_inserido == node_inserido.pai.esquerda:
                        node_inserido = node_inserido.pai
                        self._rotacionar_direita(node_inserido)

                    node_inserido.pai.cor = 0
                    node_inserido.pai.pai.cor = 1
                    self._rotacionar_esquerda(node_inserido.pai.pai)

            else:
                tio = node_inserido.pai.pai.direita
                if tio.cor == 1:
                    tio.cor = 0
                    node_inserido.pai.cor = 0
                    node_inserido.pai.pai.cor = 1
                    node_inserido = node_inserido.pai.pai

                else:
                    if node_inserido == node_inserido.pai.direita:
                        node_inserido = node_inserido.pai
                        self._rotacionar_esquerda(node_inserido)

                    node_inserido.pai.cor = 0
                    node_inserido.pai.pai.cor = 1
                    self._rotacionar_direita(node_inserido.pai.pai)

            if node_inserido == self.raiz:
                break

        self.raiz.cor = 0

    def pesquisar(self, chave):
        node = self._pesquisar_recursivo(self.raiz, chave)
        if node != self.NIL:
            print(f"Achou a chave {chave}")
            return node
        
        print(f"Não achou a chave {chave}")
        return None

    def _pesquisar_recursivo(self, node, chave):
        if node == self.NIL or chave == node.chave:
            return node
        
        if chave < node.chave:
            return self._pesquisar_recursivo(node.esquerda, chave)
        
        return self._pesquisar_recursivo(node.direita, chave)

    def mostrar(self):
        if self.raiz == self.NIL:
            print("Árvore Vazia")
            return
        
        self._imprimir_arvore(self.raiz, "", True)

    def _imprimir_arvore(self, node, prefixo="", cauda=True):
        if node.direita != self.NIL:
            prefixo_novo = prefixo + ("│   " if cauda else "    ")
            self._imprimir_arvore(node.direita, prefixo_novo, False)
        
        
        if node.cor == 0:
            texto = f"P {node.chave}"
        else:
            texto = f"V {node.chave}"

        print(prefixo + ("└── " if cauda else "┌── ") + texto)
        
        if node.esquerda != self.NIL:
            prefixo_novo = prefixo + ("    " if cauda else "│   ")
            self._imprimir_arvore(node.esquerda, prefixo_novo, True)

arvore_rubro_negra = ArvoreRubroNegra()
valores = [50, 25, 75, 15, 35, 60, 120, 10, 68, 90, 125, 83, 100, 25, 3, 7, 12, 84, 302, 1, 123, 101, 1, 7, 50]
for valor in valores:
    arvore_rubro_negra.inserir(valor)

chave = 60
print(f"Pesquisando chave {chave}:")
arvore_rubro_negra.pesquisar(chave)

arvore_rubro_negra.pesquisar(60)
arvore_rubro_negra.mostrar()