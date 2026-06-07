# Projeto da Disciplina de Banco de Dados - PPGTI/IFPB 2026.1

<div align="right">
  <strong>Aderaldo Carvalho de Melo Neto</strong> ()<br>
  <strong>Pablo Gomes de Miranda</strong> (pablo.miranda@academico.ifpb.edu.br)
</div>

## 1. Objetivo

O projeto consiste no desenvolvimento de uma aplicação orientada a dados (*data-driven application*) projetada para centralizar, tratar e expor dados abertos do poder legislativo do estado da Paraíba. O propósito final é fornecer à sociedade uma ferramenta prática e acessível para a auditoria dos gastos de agentes políticos eleitos.

A arquitetura da solução baseia-se em uma pipeline de ETL estruturada em quatro etapas fundamentais: **Extração**, que consome dados públicos via APIs REST; **Armazenamento e Persistência**, que centraliza os dados brutos e tratados no MongoDB; **Transformação**, responsável pelo processamento, limpeza e padronização; e **Entrega**, que disponibiliza as informações em um dashboard interativo para o usuário final.

O desenvolvimento deste ecossistema consolida os tópicos práticos e teóricos abordados ao longo do semestre:

1. **Pipelines Data-Driven e Metadados:** Estruturação de fluxos orientados a dados.
2. **Ingestão de Dados:** Coleta e raspagem web via APIs sob os princípios de conformidade da LGPD.
3. **Modelos de Persistência:** Avaliação, justificativa e aplicação de estruturas NoSQL.
4. **Ecossistema MongoDB:** Modelagem de documentos, execução de consultas complexas e otimização por meio de índices.

## 2. Escopo (definição do problema)

### Problema de dados

A aplicação visa centralizar e disponibilizar dados atualizados sobre os gastos realizados pelos deputados estaduais da Paraíba. O objetivo primário é fornecer à **população em geral (eleitores, jornalistas, pesquisadores e entidades de controle social)** uma ferramenta prática e acessível para o exercício da auditoria cidadã.

Atualmente, observa-se um descompasso no acompanhamento da atuação parlamentar: a atenção pública e midiática frequentemente se concentra nos altos escalões do poder executivo ou no legislativo federal, reduzindo o escrutínio sobre os representantes estaduais. Considerando o contínuo ciclo eleitoral, no qual os deputados rotineiramente buscam a reeleição ou cargos com maiores atribuições, a aplicação atende à necessidade de promover maior transparência e observabilidade sobre a destinação de recursos públicos. Dessa forma, a plataforma busca qualificar o debate político, embasar a avaliação das ações desses agentes e auxiliar o cidadão na tomada de decisões mais conscientes nas urnas.

### Solução proposta

A extração de dados é feita à partir da ingestão dados públicos disponibilizados pelo portal de dados abertos da Câmara dos Deputados via API RESTful. Os dados são armazenados no MongoDB em uma camada *staging*, transformados em uma camada *dimension* e servidos à partir de uma camada *fact* para um dashboard, que é gerido utilizando Metabase que serve também para servir cards e gráficos aos usuários finais.

### Por que documentos/MongoDB?

Escolhemos o MongoDB porque os dados de gastos públicos que consumimos via API são flexíveis e mudam com frequência, com campos opcionais ou aninhados. Ao invés de prepararmos diferentes *joins* para montar o histórico de um deputado, o modelo de documentos salva tudo o que precisamos em um único registro JSON/BSON. Isso deixa a gravação dos dados mais rápida na camada de *staging* e também agiliza as consultas que alimentam o nosso dashboard final.

## 3. Entendimento da Fonte de Dados -> FAZER

a. Fonte: origem (API, open data, web scraping, arquivo, etc.), forma de acesso e licença/uso.
b. Aspectos legais/éticos: se houver dado pessoal, registre o tratamento à luz da LGPD (base legal, anonimização/minimização). Se não houver, declare explicitamente.
c. Metadados descritivos: volume, formato, frequência de atualização, idioma, fonte original.
d. Dicionário de dados (metadados estruturais) — tabela campo | tipo | descrição | exemplo.
