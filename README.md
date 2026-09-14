# Social Media Automation

Automacao para criacao e publicacao de conteudo em redes sociais usando IA.

## Funcionalidades

- Gera legendas para feed usando GPT-4
- Gera textos para stories
- Gera imagens com DALL-E 3
- Publica automaticamente no Instagram (feed + stories)
- Publica no Facebook

## Configuracao

1. Instale as dependencias:
```bash
pip install -r requirements.txt
```

2. Copie o arquivo `.env.example` para `.env` e preencha suas chaves de API:
```bash
cp .env.example .env
```

3. Configure as seguintes variaveis no `.env`:
- `OPENAI_API_KEY`: Sua chave de API da OpenAI
- `INSTAGRAM_ACCESS_TOKEN`: Token de acesso do Instagram
- `INSTAGRAM_BUSINESS_ACCOUNT_ID`: ID da conta comercial do Instagram
- `FACEBOOK_ACCESS_TOKEN`: Token de acesso do Facebook
- `FACEBOOK_PAGE_ID`: ID da pagina do Facebook

## Uso

```bash
# Publicar no Instagram (padrao)
python main.py "dicas de produtividade"

# Publicar em multiplas plataformas
python main.py "marketing digital" -p instagram facebook

# Definir tom de voz
python main.py "educacao financeira" -t casual
```

## Tom de voz disponivel

- `profissional` (padrao)
- `casual`
- `engajante`
- `educativo`

## Estrutura do projeto

```
social_media_automation/
├── main.py                 # Script principal
├── config.py              # Configuracoes de API
├── requirements.txt       # Dependencias
├── .env.example           # Exemplo de variaveis de ambiente
└── src/
    ├── text_generator.py  # Geracao de texto com GPT
    ├── image_generator.py # Geracao de imagem com DALL-E
    └── publishers/
        ├── instagram.py   # Publicacao no Instagram
        └── facebook.py    # Publicacao no Facebook
```
