from enum import Enum

from pydantic import BaseModel, Field


class EndQuestionCategory(Enum):
    tecnologia = 'Tecnologia'
    saude = 'Saúde'
    educacao = 'Educação'
    entretenimento = 'Entretenimento'
    viagem = 'Viagem'
    historia = 'História'
    financas = 'Finanças'
    relacionamentos = 'Relacionamentos'
    moda = 'Moda'
    comida = 'Comida'
    fitness = 'Fitness'
    arte = 'Arte'
    psicologia = 'Psicologia'
    programacao = 'Programação'
    musica = 'Música'
    literatura = 'Literatura'
    meio_ambiente = 'Meio Ambiente'
    paternidade = 'Paternidade'
    jogos = 'Jogos'
    politica = 'Política'
    futebol = 'Futebol'
    outros = 'Outros'
    carro = 'Carro'
    motocicleta = 'Motocicleta'
    veiculo = 'Veículo'
    redes_sociais = 'Redes Sociais'
    humor = 'Humor'
    piadas = 'Piadas'
    economia = 'Economia'


class AboutCategory(BaseModel):
    """
    Representa o tópico da pergunta.

    Atributos:
        topic (EndQuestionCategory): O tópico da pergunta, que deve ser um dos valores definidos na
        classe EndQuestionCategory.
    """

    topic: EndQuestionCategory = Field(
        ..., description='Tópico da pergunta conforme categorizado'
    )


class StartQuestionCategory(Enum):
    Scientific = 'Computer science scientific article'
    NonScientific = 'Non-scientific'


class AboutScience(BaseModel):
    """
    Representa a categoria da pergunta, indicando se está relacionada a artigos científicos de ciências da computação.
    """

    category: StartQuestionCategory = Field(
        ...,
        description='Indica se a pergunta é sobre artigos científicos de ciências da computação ou não científica.',
    )
