# Projeto da Disciplina de Banco de Dados - PPGTI/IFPB 2026.1

<div align="right">
  <strong>Aderaldo Carvalho de Melo Neto</strong> (aderaldo.carvalho@academico.ifpb.edu.br)<br>
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

A extração de dados é feita à partir da ingestão dados públicos disponibilizados pelo portal de [Dados Abertos da Câmara dos Deputados](https://dadosabertos.camara.leg.br) via API RESTful. Os dados são armazenados no MongoDB em uma camada *staging*, transformados em uma camada *dimension* e servidos à partir de uma camada *fact* para um dashboard, que é gerido utilizando Metabase que serve também para servir cards e gráficos aos usuários finais.

### Por que documentos/MongoDB?

Escolhemos o MongoDB porque os dados de gastos públicos que consumimos via API são flexíveis e mudam com frequência, com campos opcionais ou aninhados. Ao invés de prepararmos diferentes *joins* para montar o histórico de um deputado, o modelo de documentos salva tudo o que precisamos em um único registro JSON/BSON. Isso deixa a gravação dos dados mais rápida na camada de *staging* e também agiliza as consultas que alimentam o nosso dashboard final.

## 3. Entendimento da Fonte de Dados

### a. Fonte

Os dados públicos utilizados são consumidos a partir do portal [Dados Abertos da Câmara dos Deputados](https://dadosabertos.camara.leg.br). A ingestão ocorre por meio do endpoint central [https://dadosabertos.camara.leg.br/api/v2](https://dadosabertos.camara.leg.br/api/v2), que implementa uma arquitetura RESTful e oferece suporte aos formatos JSON e XML. Para fins de engenharia de dados e controle de tráfego, a API adota uma paginação padrão com retorno de 15 itens por página e um limite máximo de 100 registros por requisição. Em relação à propriedade intelectual e governança, o portal não especifica uma licença de uso restritiva (como Creative Commons), caracterizando os ativos estritamente como dados públicos de livre acesso. O fornecimento gratuito visa incentivar a sociedade civil, pesquisadores e desenvolvedores a construírem soluções que promovam a transparência sobre votações, atuação parlamentar e o monitoramento de gastos reembolsados com recursos públicos.

### b. Aspectos legais/éticos

O portal deixa claro que não há dados pessoais dos deputados na sessão de *FAQ* conforme disponibilizamos abaixo:

"Os dados abertos incluem as informações pessoais de parlamentares e colaboradores? Não, pelo menos por enquanto. Existem restrições às informações que podem ser divulgadas, especialmente as de caráter pessoal e/ou familiar. O Ato da Mesa 45/2012 é atualmente o principal dos marcos regulatórios da Câmara que definem quais informações podem ser tornadas públicas ou não" (https://dadosabertos.camara.leg.br/faq/faq-home.html#r5 acesso em 7 de junho de 2026).

Desse modo não há necessidade de anonimização/minimização dos dados.

### c. Metadados descritivos: volume, formato, frequência de atualização, idioma, fonte original.

- Volume: ?

- Formato: JSON ou XML;

- Frequência de Atualização: ?;

- Idioma: Português;

- Fonte original: segundo FAQ, "diretamente das bases de dados que são alimentadas por diversos sistemas de uso interno da Câmara" (https://dadosabertos.camara.leg.br/faq/faq-home.html#r5 acesso em 7 de junho de 2026).

### d. Dicionário de dados

#### Coleção: `deputados` (Dados Cadastrais e Perfil)

| Campo | Tipo | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| `_id` | Integer | Identificador único do deputado na Câmara (Chave Primária). | `178910` |
| `nome` | String | Nome civil completo do parlamentar. | `Aguinaldo Ribeiro` |
| `nomeEleitoral` | String | Nome formato de urna utilizado pelo político. | `AGUINALDO RIBEIRO` |
| `siglaPartido` | String | Sigla do partido político atual do deputado. | `PP` |
| `siglaUf` | String | Estado (Unidade da Federação) que o elegeu. | `PB` |
| `idLegislatura` | Integer | Identificador da legislatura corrente. | `57` |
| `urlFoto` | String | Link direto para a imagem oficial do parlamentar. | `https://www.camara.leg.br/internet/deputado/bandera/178910.jpg` |
| `email` | String | Endereço de e-mail institucional oficial. | `dep.aguinaldoribeiro@camara.leg.br` |
| `profissoes` | Array (String) | Lista de profissões declaradas pelo parlamentar. | `["Engenheiro Civil", "Administrador"]` |

---

#### Coleção: `despesas` (Histórico de Gastos e Reembolsos)

| Campo | Tipo | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| `_id` | ObjectId | Identificador único do registro gerado automaticamente pelo MongoDB. | `66637ef89a1c2d3e4f5a6b7c` |
| `deputadoId` | Integer | ID de referência do deputado que gerou a despesa (Chave Estrangeira). | `178910` |
| `ano` | Integer | Ano em que a despesa foi realizada. | `2026` |
| `mes` | Integer | Mês em que a despesa foi realizada. | `5` |
| `tipoDespesa` | String | Categoria/Classificação do gasto efetuado. | `COMBUSTÍVEIS E LUBRIFICANTES` |
| `dataEmissao` | String (Date) | Data de emissão do documento fiscal (padrão ISO 8601). | `2026-05-20` |
| `numDocumento` | String | Número da nota fiscal, recibo ou comprovante do gasto. | `459821` |
| `nomeFornecedor` | String | Razão social ou nome do fornecedor/prestador do serviço. | `POSTO TAMBAU LTDA` |
| `cnpjCpfFornecedor` | String | Inscrição do CNPJ ou CPF do fornecedor emitente. | `00123456000189` |
| `valorDocumento` | Double | Valor bruto total registrado na nota fiscal. | `250.50` |
| `valorGlosa` | Double | Valor retido ou rejeitado pela auditoria da Câmara. | `0.00` |
| `valorLiquido` | Double | Valor efetivamente reembolsado ao parlamentar. | `250.50` |
| `urlDocumento` | String | Link para o documento digitalizado (quando disponível). | `https://www.camara.leg.br/cota-parlamentar/doc/123.pdf` |

## 4. Requisitos de dados (perguntas que a aplicação responde)

Pensando na legislatura atual (2022 - 2026) no contexto do estado da Paraíba:

1. Quais são as 5 maiores categorias que possuem mais despesas?

2. Quais são os 5 políticos com maiores despesas?

3. Quais sãos os 5 políticos com menores despesas?

4. Quais são os 5 principais fornecedores?

5. A média da cota parlamentar da Paraíba é menor ou maior do quê a cota nacional?

6. Qual foi o ano com maior despesa?