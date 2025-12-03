 Seu Próximo Passo: Criar os Dashboards

  Agora você precisa visualizar esses dados. Siga os passos abaixo:

  1. Roteiro de Execução

  Antes de criar os dashboards, você precisa garantir que todo o pipeline seja executado na ordem correta.

   1. Inicie os Serviços: No terminal, na raiz do projeto, execute:
   1     docker-compose up -d --build
      Aguarde alguns minutos para que todos os contêineres (Postgres, ThingsBoard, etc.) iniciem completamente.

   2. Crie as Tabelas do Banco: Execute o script para inicializar a tabela thermal_measurements:
   1     python3 scripts/init_tables.py

   3. Treine e Registre o Modelo: Execute o notebook para treinar o RandomForestClassifier e registrá-lo no MLflow.
   1     # Se quiser, pode executar o notebook diretamente, ou via linha de comando:
   2     jupyter nbconvert --to notebook --execute notebooks/pipeline_ml.ipynb
      Isso garante que o modelo "random_forest_model" esteja disponível no MLflow para a API de predição.

   4. Ingira os Dados do INMET: Rode o script para buscar os dados e enviá-los para o banco de dados e para o ThingsBoard.
   1     python3 scripts/ingest_data.py

  2. Configuração do Dashboard no ThingsBoard

   1. Acesse o ThingsBoard: Abra http://localhost:8080 no seu navegador.
   2. Login: Use as credenciais padrão:
       * Usuário: tenant@thingsboard.org
       * Senha: tenant
   3. Verifique o Dispositivo:
       * No menu à esquerda, vá para Devices.
       * Você verá um dispositivo chamado "Estação INMET Recife", que foi criado automaticamente pelo script
         ingest_data.py.
       * Clique nele e vá para a aba "Latest telemetry". Você deverá ver os dados que o script enviou (temperatura,
         umidade, etc.).
   4. Crie seu Dashboard:
       * Vá para Dashboards, clique no + para criar um novo dashboard. Dê um nome a ele, como "Análise de Conforto
         Térmico".
       * Abra o dashboard e entre no modo de edição (clique no lápis no canto inferior direito).
       * Adicione Widgets: Clique em "Add new widget". Explore os pacotes de widgets (Charts, Gauges, etc.).
       * Para cada widget, você precisará:
           * Selecionar o dispositivo ("Estação INMET Recife").
           * Selecionar a chave de telemetria que deseja visualizar (ex: temperature, humidity).
           * Configure o widget para ter uma boa aparência, atendendo aos critérios de "qualidade, estética e clareza" da
             sua avaliação. Crie gráficos de linha para séries temporais e gauges para valores atuais.

  3. Análise Preditiva no Trendz

  O Trendz é usado para análises mais complexas e preditivas sobre os dados do ThingsBoard.

   1. Acesse o Trendz: Abra http://localhost:8888 no seu navegador.
   2. Explore os Dados: O Trendz já estará conectado ao ThingsBoard. Você pode criar "Views" para explorar os dados da sua
      estação.
   3. Crie Visualizações Preditivas: O objetivo aqui é usar os recursos do Trendz para análise preditiva.
       * Crie um gráfico de linha com a temperatura histórica.
       * Use a função "Forecast" do Trendz para prever a tendência da temperatura para os próximos dias.
       * Sugestão de Melhoria: Para comparar o modelo do Trendz com o seu modelo de ML, você poderia criar um segundo
         dispositivo no ThingsBoard, chamado "Predições do Modelo", e modificar a API (prediction.py) para, além de
         retornar a predição, enviá-la também como telemetria para este novo dispositivo. Assim, você poderia plotar no
         mesmo gráfico a predição do Trendz e a predição do seu RandomForestClassifier.

  ---