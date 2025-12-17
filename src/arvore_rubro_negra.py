# Marcos Vinicius Brito de Araujo - 202404940009
# Maurício Aires Pinheiro - 202404940003

import sys

sys.stdout.reconfigure(encoding='utf-8')

class NodeRubroNegra:
    def __init__(self, chave):
        self.chave = chave
        self.esquerda = None
        self.direita = None
        self.pai = None
        self.cor = 1

class ArvoreRubroNegra:
    def __init__(self):
        self.NIL = NodeRubroNegra(None)
        self.NIL.cor = 0
        self.raiz = self.NIL

    def _minimo(self, node):
        while node.esquerda != self.NIL:
            node = node.esquerda
        return node

    def _transplantar(self, u, v):
        if u.pai is None:
            self.raiz = v
        elif u == u.pai.esquerda:
            u.pai.esquerda = v
        else:
            u.pai.direita = v
        v.pai = u.pai

    def _rotacionar_esquerda(self, node_desbalanceado):
        pivo = node_desbalanceado.direita
        node_desbalanceado.direita = pivo.esquerda
        if pivo.esquerda != self.NIL:
            pivo.esquerda.pai = node_desbalanceado

        pivo.pai = node_desbalanceado.pai
        if node_desbalanceado.pai is None:
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
        if node_desbalanceado.pai is None:
            self.raiz = pivo
        elif node_desbalanceado == node_desbalanceado.pai.direita:
            node_desbalanceado.pai.direita = pivo
        else:
            node_desbalanceado.pai.esquerda = pivo

        pivo.direita = node_desbalanceado
        node_desbalanceado.pai = pivo

    def inserir(self, chave):
        novo_node = NodeRubroNegra(chave)
        novo_node.esquerda = self.NIL
        novo_node.direita = self.NIL
        novo_node.pai = None
        novo_node.cor = 1
        
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
        if pai_aux is None:
            self.raiz = novo_node
        elif novo_node.chave < pai_aux.chave:
            pai_aux.esquerda = novo_node
        else:
            pai_aux.direita = novo_node

        if novo_node.pai is None:
            novo_node.cor = 0
            return

        if novo_node.pai.pai is None:
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

    def remover(self, chave):
        z = self._pesquisar_recursivo(self.raiz, chave)
        if z == self.NIL:
            print(f"Chave {chave} não encontrada.")
            return

        y = z
        y_cor_original = y.cor
        
        if z.esquerda == self.NIL:
            x = z.direita
            self._transplantar(z, z.direita)
        elif z.direita == self.NIL:
            x = z.esquerda
            self._transplantar(z, z.esquerda)
        else:
            y = self._minimo(z.direita)
            y_cor_original = y.cor
            x = y.direita
            if y.pai == z:
                x.pai = y
            else:
                self._transplantar(y, y.direita)
                y.direita = z.direita
                y.direita.pai = y
            
            self._transplantar(z, y)
            y.esquerda = z.esquerda
            y.esquerda.pai = y
            y.cor = z.cor

        if y_cor_original == 0:
            self._ajustar_remocao(x)

    def _ajustar_remocao(self, x):
        while x != self.raiz and x.cor == 0:
            if x == x.pai.esquerda:
                w = x.pai.direita
                if w.cor == 1:
                    w.cor = 0
                    x.pai.cor = 1
                    self._rotacionar_esquerda(x.pai)
                    w = x.pai.direita
                
                if w.esquerda.cor == 0 and w.direita.cor == 0:
                    w.cor = 1
                    x = x.pai
                else:
                    if w.direita.cor == 0:
                        w.esquerda.cor = 0
                        w.cor = 1
                        self._rotacionar_direita(w)
                        w = x.pai.direita
                    
                    w.cor = x.pai.cor
                    x.pai.cor = 0
                    w.direita.cor = 0
                    self._rotacionar_esquerda(x.pai)
                    x = self.raiz
            else:
                w = x.pai.esquerda
                if w.cor == 1:
                    w.cor = 0
                    x.pai.cor = 1
                    self._rotacionar_direita(x.pai)
                    w = x.pai.esquerda
                
                if w.direita.cor == 0 and w.esquerda.cor == 0:
                    w.cor = 1
                    x = x.pai
                else:
                    if w.esquerda.cor == 0:
                        w.direita.cor = 0
                        w.cor = 1
                        self._rotacionar_esquerda(w)
                        w = x.pai.esquerda
                    
                    w.cor = x.pai.cor
                    x.pai.cor = 0
                    w.esquerda.cor = 0
                    self._rotacionar_direita(x.pai)
                    x = self.raiz
        
        x.cor = 0

    def pesquisar(self, chave):
        node = self._pesquisar_recursivo(self.raiz, chave)
        if node != self.NIL:
            print(f"Chave {chave} ({'Vermelho' if node.cor == 1 else 'Preto'}) encontrada.")
            return node
        
        print(f"Chave {chave} não encontrada.")
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
        
        cor_texto = "V" if node.cor == 1 else "P"
        print(prefixo + ("└── " if cauda else "┌── ") + f"{cor_texto} {node.chave}")
        
        if node.esquerda != self.NIL:
            prefixo_novo = prefixo + ("    " if cauda else "│   ")
            self._imprimir_arvore(node.esquerda, prefixo_novo, True)


arvore_rubro_negra = ArvoreRubroNegra()

print("1. Inserção")
valores = [20, 15, 25, 10, 5, 1, 30, 35] 
for v in valores:
    arvore_rubro_negra.inserir(v)
arvore_rubro_negra.mostrar()

print("2. Pesquisa")
arvore_rubro_negra.pesquisar(25)
arvore_rubro_negra.pesquisar(99)

print("3. Remoção")
print("Removendo 1:")
arvore_rubro_negra.remover(1)
arvore_rubro_negra.mostrar()

print("Removendo 25:")
arvore_rubro_negra.remover(25)
arvore_rubro_negra.mostrar()

print("Removendo a raiz:")
raiz_chave = arvore_rubro_negra.raiz.chave
arvore_rubro_negra.remover(raiz_chave)
arvore_rubro_negra.mostrar()