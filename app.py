import csv

class SistemaAlocacaoHorario:
    def __init__(self, membros_file, alocacoes_file):
        self.membros_file = membros_file
        self.alocacoes_file = alocacoes_file
        self.membros = self._carregar_membros()
        self.alocacoes = self._carregar_alocacoes()

    def _carregar_membros(self):
        membros = {}
        with open(self.membros_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                membros[row['nome']] = Membro(row['nome'], row['senioridade'], row['cargo'], int(row['horas']))
        return membros

    def _carregar_alocacoes(self):
        alocacoes = []
        with open(self.alocacoes_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                membro = self.membros[row['nome']]
                adv = Alocacao(membro, int(row['horas']), row['motivo'])
                membro.adicionar_alocacao(adv)
                alocacoes.append(adv)
        return alocacoes

    def _salvar_membros(self):
        with open(self.membros_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['nome', 'senioridade', 'cargo', 'horas'])
            for membro in self.membros.values():
                writer.writerow([membro.nome, membro.senioridade, membro.cargo, membro.horas])

    def _salvar_alocacoes(self):
        with open(self.alocacoes_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['nome', 'horas', 'motivo'])
            for adv in self.alocacoes:
                writer.writerow([adv.membro.nome, adv.horas, adv.motivo])

    def cadastrar_membro(self, nome, senioridade, cargo, horas):
        if nome in self.membros:
            raise ValueError('Membro já cadastrado')
        self.membros[nome] = Membro(nome, senioridade, cargo, horas)
        self._salvar_membros()

    def cadastrar_alocacao(self, nome_membro, horas, motivo):
        membro = self.membros.get(nome_membro)
        if not membro:
            raise ValueError('Membro não encontrado')
        alocacao = Alocacao(membro, horas, motivo)
        membro.adicionar_alocacao(alocacao)
        self.alocacoes.append(alocacao)
        self._salvar_alocacoes()

    def editar_membro(self, nome, senioridade, cargo, horas):
        membro = self.membros.get(nome)
        if not membro:
            raise ValueError('Membro não encontrado')
        membro.senioridade = senioridade
        membro.cargo = cargo
        membro.horas = horas
        self._salvar_membros()

    def editar_alocacao(self, nome_membro, indice_alocacao, horas, motivo):
        membro = self.membros.get(nome_membro)
        if not membro:
            raise ValueError('Membro não encontrado')
        if indice_alocacao < 0 or indice_alocacao >= len(membro.alocacoes):
            raise ValueError('Índice de alocação inválido')
        alocacao = membro.alocacoes[indice_alocacao]
        alocacao.horas = horas
        alocacao.motivo = motivo
        self._salvar_alocacoes()

    def buscar_membro_por_nome(self, nome):
        membro = self.membros.get(nome)
        if not membro:
            raise ValueError('Membro não encontrado')
        return membro

    def buscar_alocacoes_por_nome(self, nome):
        membro = self.membros.get(nome)
        if not membro:
            raise ValueError('Membro não encontrado')
        return membro.alocacoes


class Membro:
    def __init__(self, nome, senioridade, cargo, horas):
        self.nome = nome
        self.senioridade = senioridade
        self.cargo = cargo
        self.horas = horas
        self.alocacoes = []

    def adicionar_alocacao(self, alocacao):
        self.alocacoes.append(alocacao)
        self.horas += alocacao.horas


class Alocacao:
    def __init__(self, membro, horas, motivo):
        self.membro = membro
        self.horas = horas
        self.motivo = motivo

    def __str__(self):
        return f'Alocação - Membro: {self.membro.nome} - Horas: {self.horas} - Motivo: {self.motivo}'


import streamlit as st

MEMBROS_FILE = 'membros.csv'
ALOCACOES_FILE = 'alocacoes.csv'

sistema = SistemaAlocacaoHorario(MEMBROS_FILE, ALOCACOES_FILE)

def cadastrar_membro():
    nome = st.text_input('Nome')
    senioridade = st.text_input('senioridade')
    cargo = st.text_input('Cargo')
    horas = st.number_input('Horas', value=0)
    if st.button('Cadastrar'):
        try:
            sistema.cadastrar_membro(nome, senioridade, cargo, horas)
            st.success('Membro cadastrado com sucesso!')
        except ValueError as e:
            st.error(str(e))

def cadastrar_alocacao():
    nome_membro = st.text_input('Nome do membro')
    horas = st.number_input('Horas', value=0)
    motivo = st.text_input('Motivo')
    if st.button('Cadastrar'):
        try:
            sistema.cadastrar_alocacao(nome_membro, horas, motivo)
            st.success('Alocação cadastrada com sucesso!')
        except ValueError as e:
            st.error(str(e))

def editar_membro():
    nome = st.text_input('Nome')
    senioridade = st.text_input('senioridade')
    cargo = st.text_input('Cargo')
    horas = st.number_input('Horas', value=0)
    if st.button('Editar'):
        try:
            sistema.editar_membro(nome, senioridade, cargo, horas)
            st.success('Membro editado com sucesso!')
        except ValueError as e:
            st.error(str(e))

def editar_alocacao():
    nome_membro = st.text_input('Nome do membro')
    indice_alocacao = st.number_input('Índice da alocação', value=0)
    horas = st.number_input('Horas', value=0)
    motivo = st.text_input('Motivo')
    if st.button('Editar'):
        try:
            sistema.editar_alocacao(nome_membro, indice_alocacao, horas, motivo)
            st.success('Alocação editada com sucesso!')
        except ValueError as e:
            st.error(str(e))

def buscar_membro():
    nome = st.text_input('Nome')
    if st.button('Buscar'):
        try:
            membro = sistema.buscar_membro_por_nome(nome)
            st.write(f'Nome: {membro.nome}')
            st.write(f'senioridade: {membro.senioridade}')
            st.write(f'Cargo: {membro.cargo}')
            st.write(f'Horas: {membro.horas}')
        except ValueError as e:
            st.error(str(e))

def buscar_alocacoes():
    nome = st.text_input('Nome')
    if st.button('Buscar'):
        try:
            alocacoes = sistema.buscar_alocacoes_por_nome(nome)
            for alocacao in alocacoes:
                st.write(str(alocacao))
        except ValueError as e:
            st.error(str(e))

def main():
    st.title('Sistema de Alocação de Horário')
    opcoes = ['Cadastrar Membro', 'Cadastrar Alocação', 'Editar Membro', 'Editar Alocação', 'Buscar Membro', 'Buscar Alocações']
    escolha = st.sidebar.selectbox('Escolha uma opção', opcoes)
    if escolha == 'Cadastrar Membro':
        cadastrar_membro()
    elif escolha == 'Cadastrar Alocação':
        cadastrar_alocacao()
    elif escolha == 'Editar Membro':
        editar_membro()
    elif escolha == 'Editar Alocação':
        editar_alocacao()
    elif escolha == 'Buscar Membro':
        buscar_membro()
    elif escolha == 'Buscar Alocações':
        buscar_alocacoes()

if __name__ == '__main__':
    main()
