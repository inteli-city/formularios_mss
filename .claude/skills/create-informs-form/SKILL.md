---
name: create-informs-form
description: Criar formulários no microserviço MSS Formulários (Informs) via API REST, com seleção automática de ambiente (dev ou homolog), suporte completo aos 10 tipos de field, e escolha de posse (OWNED direcionado, ou OPEN no pool — feature Uberlândia/SGISV). Use sempre que o usuário pedir para criar formulários, popular dados de teste, ou rodar POST de formulários no Informs/mss-formularios. Triggers comuns: "cria N formulários no informs", "popula forms na API", "POST de formulário no dev/homolog", "cria formulários para o user_id X", "cria um form no pool/sem dono", "manda alguns forms pro Informs", ou qualquer menção a `mss-formularios` com intenção de criação.
---

# Create Informs Form

Cria formulários no microserviço MSS Formulários da Intelicity via POST autenticado, escolhendo automaticamente a URL correta para o ambiente (dev ou homolog) e montando o body conforme as regras de cada `field_type`.

## Quando usar

Use esta skill sempre que precisar:
- Criar 1 ou mais formulários via API no Informs
- Popular dados de teste em dev/homolog para um `user_id` específico, ou sem dono (pool)
- Rodar POSTs em massa para validar deploys, fluxos do app, ou cenários de QA

Se o usuário não disser o ambiente, **pergunte** — é a primeira coisa que precisa estar clara.

## Inputs necessários

Antes de chamar a API, confirme que tem:

1. **Ambiente** — `dev` ou `homolog`
2. **Bearer token** — **sempre estritamente necessário**, mesmo quando o form vai ser criado sem dono (`user_id` omitido). É o token de quem loga (`sub`/grupo `FORMULARIOS`) que autentica a chamada e vira o `created_by` — não existe criação anônima. Obtido logando no Gates do ambiente pelo browser do Claude Code (ver "Como obter o token" abaixo). Se o usuário já colar um token pronto, pule o login e use o que foi passado.
3. **Posse do formulário — pergunte se não estiver claro**:
   - **OWNED (direcionado)** — tem um dono desde a criação. Se o usuário não disser um destinatário, usa o próprio `sub` do token (cria pra si mesmo). Comportamento padrão/histórico, sempre funciona.
   - **OPEN (pool, sem dono)** — feature Uberlândia/SGISV (Fase 1). Omite `user_id` no payload; o form nasce com `possession=OPEN`, visível a qualquer usuário autenticado via `GET /forms?scope=pool` até alguém reivindicar (`claim`) ou um gestor atribuir (`assign`). **Só funciona se o `system` tiver `SystemConfig.allow_unassigned_forms=True`** (hoje isso não é geral — GAIA e outros systems legados podem não ter essa config em `dev`); se faltar, a API responde `400 "Parâmetro ausente: user_id"`. Nesse caso, **não insista tentando de novo sem user_id** — crie o form OWNED (pro próprio token) e em seguida chame `POST /forms/{formId}/release` pra devolver ao pool (mesmo resultado final: `possession=OPEN`). Ver "Criar no pool" abaixo.
4. **Quantidade e/ou tema dos formulários** — quantos criar e que tipo (ex: "5 forms variados", "3 de inspeção predial")

## Como obter o token (login via browser)

1. Abra o browser do Claude Code na URL do Gates correspondente ao ambiente:

| Ambiente | URL de login do Gates |
|----------|------------------------|
| `dev` | `https://dev.gatesauth.com` |
| `homolog` | `https://homolog.gatesauth.com` |
| `prod` | `https://gatesauth.com` |

2. Avise o usuário que a aba está aberta e peça pra ele logar com a própria conta. Nunca digite credenciais por ele — só espere ele confirmar que terminou.
3. Com o login feito, extraia o `idToken` do localStorage (a chave vem com o client id embutido, então procure por substring em vez de um nome fixo):

   ```js
   const key = Object.keys(localStorage).find(k => k.includes('idToken'));
   localStorage.getItem(key);
   ```

4. Esse valor é o Bearer token. Decodifique o segundo segmento do JWT (base64) pra pegar o `sub` — é o `user_id` padrão dos formulários OWNED (item 3 acima), a menos que o usuário peça outro destinatário.
5. Confira se `cognito:groups` no payload do token inclui `FORMULARIOS` — sem isso a API responde 403 (ver "Erros comuns").

## URLs por ambiente

| Ambiente | Base URL |
|----------|----------|
| `dev` | `https://kuoea48f89.execute-api.sa-east-1.amazonaws.com/prod/mss-formularios` |
| `homolog` | `https://ggbkn1e8p9.execute-api.sa-east-1.amazonaws.com/prod/mss-formularios` |

Endpoint de criação: `POST {base_url}/forms`

Documentação Swagger: `{base_url}/docs`

## Como executar

Para criar os formulários, rode `curl` em sequência (ou em paralelo se forem muitos):

```bash
curl -s -w "\nHTTP:%{http_code}\n" -X POST "$BASE/forms" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{...payload...}'
```

Após cada chamada, **verifique o HTTP status** — `201` é sucesso. Se vier `400`, leia a mensagem de erro: geralmente diz qual parâmetro está faltando (ex: `"Parâmetro ausente: file_type"`) e basta adicionar o campo no JSON e tentar de novo — **exceção**: `400 "Parâmetro ausente: user_id"` ao tentar criar OPEN não se corrige adicionando o campo de volta (isso é só recriar OWNED); siga o fallback descrito em "Criar no pool" abaixo.

Ao terminar, mostre uma tabela resumo com: número, título, ID retornado, sistema, prioridade, posse (OWNED/OPEN) e quantas seções/fields o form tem.

## Estrutura mínima do payload

```json
{
  "form_title": "Título do formulário",
  "user_id": "<UUID do destinatário>",
  "system": "GAIA",
  "city": "São Paulo",
  "street": "Endereço completo",
  "latitude": -23.56,
  "longitude": -46.65,
  "priority": 1,
  "justifications": [
    {"option": "Texto da opção", "required_image": false, "required_text": false}
  ],
  "sections": [
    {
      "section_id": 1,
      "fields": [
        {"field_type": "TEXT_FIELD", "label": "Descrição", "required": true, "key": "descricao", "order": 1}
      ]
    }
  ]
}
```

### Valores válidos

- **system** (string livre, mas valores comuns na plataforma): `GAIA`, `SGC`, `GEOVISTA`, `INTELIFLEETS`
- **priority** (int): `0` Low, `1` Medium, `2` High, `3` Emergency
- **user_id** (opcional): presente → form nasce `OWNED`; ausente → form nasce `OPEN` **se** o `system` permitir (ver item 3 dos Inputs)

### Campos opcionais do form

- `template` (UUID de um template existente — se ausente ou inválido, `sections` é obrigatório)
- `observation` (string)
- `expiration_date` (timestamp em ms)
- `information_fields` (array — ver `references/field-schemas.md`)

## Criar no pool (possession=OPEN)

1. Monte o payload **sem o campo `user_id`** (não mande `null` — omita a chave).
2. Tente o `POST /forms` normalmente.
3. Se vier `201`: pronto, já nasceu `OPEN`. Confirme no corpo da resposta (`"possession": "OPEN"`).
4. Se vier `400 "Parâmetro ausente: user_id"`: esse `system` ainda não tem `allow_unassigned_forms=True` configurado em `dev`/`homolog`. Fallback (mesmo resultado final):
   a. Recrie o payload **com** `user_id` = `sub` do próprio token (form nasce `OWNED`).
   b. Chame `POST /forms/{formId}/release` (mesmo token) — devolve o form ao pool, `possession` vira `OPEN`, conteúdo da seção-base é descartado (RN-UBE-004, comportamento esperado do `release`).
   c. Avise o usuário que usou o fallback e por quê (não é erro seu nem do form — é o `system` que ainda não está habilitado pra criação direta sem dono).

## Field types

Cada `field_type` tem campos obrigatórios próprios além dos comuns (`field_type`, `label`, `required`, `key`, `order`). Os 10 tipos suportados e seus requisitos extras estão em `references/field-schemas.md` — **leia esse arquivo antes de montar o payload se for usar qualquer field além de TEXT_FIELD/DATE_FIELD/CHECKBOX_FIELD/SWITCH_BUTTON_FIELD**.

Resumo rápido dos que mais quebram quando esquecidos:
- `FILE_FIELD` → exige `file_type` (`IMAGE` ou `DOCUMENT`), `min_quantity`, `max_quantity`
- `NUMBER_FIELD` → exige `decimal` (bool)
- `DROPDOWN_FIELD`, `TYPEAHEAD_FIELD`, `RADIO_GROUP_FIELD`, `CHECKBOX_GROUP_FIELD` → exigem `options` (array)

## Exemplos prontos

Em `references/example-payloads.md` há exemplos completos prontos para copiar e adaptar:
- Formulário simples (1 section, TEXT + FILE)
- Formulário médio (3 sections, mix de tipos)
- Formulário com `information_fields`
- Formulário no pool (`possession=OPEN`, sem `user_id`)

## Fluxo recomendado

1. **Pergunte o ambiente** se o usuário não disse
2. **Pergunte a posse** (OWNED direcionado, ou OPEN no pool) se não estiver claro — ver item 3 dos Inputs
3. **Login via browser** no Gates do ambiente pra obter o token (pule se já tiver um em mãos) — token é obrigatório nos dois casos
4. **Confirme** a quantidade e o tema dos formulários
5. **Monte os payloads** variando título, sistema, cidade, prioridade — não envie 5 cópias idênticas
6. **Execute em paralelo** quando possível (curl em um único comando bash com `&&` ou múltiplos blocos)
7. **Reporte o resultado** em tabela: # | Título | ID | Sistema | Prioridade | Posse | HTTP

## Erros comuns e como reagir

| Erro | Causa | Correção |
|------|-------|----------|
| `400 "Parâmetro ausente: file_type"` | FILE_FIELD sem `file_type` | Adicionar `"file_type": "IMAGE"` ou `"DOCUMENT"` |
| `400 "Parâmetro ausente: decimal"` | NUMBER_FIELD sem `decimal` | Adicionar `"decimal": true` ou `false` |
| `400 "Parâmetro ausente: options"` | DROPDOWN/RADIO/CHECKBOX_GROUP/TYPEAHEAD sem `options` | Adicionar `"options": ["A", "B"]` |
| `400 "Parâmetro ausente: sections"` | template inválido e sem sections | Fornecer `sections` ou template UUID válido |
| `400 "Parâmetro ausente: user_id"` | Tentou criar `OPEN` (sem `user_id`) num `system` sem `allow_unassigned_forms=True` | Ver "Criar no pool" — criar OWNED e depois `release` |
| `401/403` | Token inválido, expirado, ou sem o grupo `FORMULARIOS` | Repetir o login no Gates (passo "Como obter o token") e extrair um token novo |

## Notas importantes

- O `user_id` do payload é o **destinatário** do formulário; o `created_by` é preenchido pelo backend a partir do `sub` do token — sempre a partir do token, nunca do payload. Por padrão (OWNED sem destinatário informado) os dois são a mesma pessoa (quem logou).
- O backend exige o grupo Cognito `FORMULARIOS` — se o token não tiver, dá 403.
- Não tente upar arquivos: `FILE_FIELD` na criação só declara o campo. Upload de fato acontece na submissão (`/forms/{id}/submit`) via presigned URL.
- Status inicial do formulário é sempre `PENDING`.
- `possession` (OPEN/OWNED) é um eixo de estado independente de `status` — um form pode estar `PENDING` e `OPEN` (no pool) ao mesmo tempo.
