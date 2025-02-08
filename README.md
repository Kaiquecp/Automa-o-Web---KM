Nessa automação, o código está separado em 3 partes:

Maxtrack.py: Entra no site do rastreador, faz login, aplica os filtros da data de hoje, aperta em filtrar, baixa o relatório em CSV, e salva na máquina.

KM_CSV.py: Integra com o Maxtrack.py, após o arquivo csv salvo na máquina, ele pega esse arquivo CSV, seleciona as colunas placas e KM, todas as placas repetidas com KM particionado ele une os KM em cada placa, tirando a duplicidade e salva em um arquivo excel XLSX.

KM_CSV_DIA: Integra com o KM_CSV e faz todo processo do inicio, executando o Maxtrack, depois o KM_CSV, e então ele pega esse arquivo XLSX e compara com a tabela SQL do banco de dados, então ele coloca as placas, os KM, e mantem as colunas com as informações
restantes do cavalo como: ultima cerca, nome do responsavel, entre outros, filtra as placas que não bateram a meta de acordo com o horário, e por fim adiciona uma coluna com lista suspensa com justificativas do porque que essa placa não bateu o KM. Após isso
é salvo em um arquivo XLSX e enviado por email.
