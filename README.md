# tmdb-api-chall

## 📂 Dataset

Este projeto utiliza o dataset TMDB Movies disponível no Kaggle:

🔗 [TMDB Movies Dataset (930k filmes)](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies)

Após o download, coloque o arquivo `.csv` dentro da pasta `data/`.

## 🧠 Decisões Técnicas

- O dataset original contém 24 colunas. Após análise, selecionei apenas as colunas relevantes para o escopo da aplicação.
- Foram mantidas as seguintes colunas:
  - `id`, `title`, `release_date`, `vote_average`, `vote_count`, `status`, `runtime`, `adult`, `budget`, `revenue`, `original_language`, `popularity`
  - `genres` (normalizado em tabela separada)
- As demais colunas foram ignoradas por apresentarem baixa completude ou não agregarem valor para os objetivos da API.
