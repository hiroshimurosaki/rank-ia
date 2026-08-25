class Image:
  def __init__(self, caminho, largura, altura):
    self.caminho = caminho
    self.largura = largura
    self.altura = altura

  def alterar_tamanho(self, nova_largura, nova_altura):
    self.largura = nova_largura
    self.altura = nova_altura

  def rotacionar(self, graus):
    _ = graus  # placeholder — lógica de rotação seria implementada aqui


class Animal:
  def __init__(self, nome, pernas, quantidade, imagem: Image):
    self.nome = nome
    self.pernas = pernas
    self.quantidade = quantidade
    self.imagem = imagem  # Animal tem uma Image, mas não sabe manipulá-la

  def calcular_pernas(self):
    return self.pernas * self.quantidade

  def calcular_olhos(self):
    return self.quantidade * 2

