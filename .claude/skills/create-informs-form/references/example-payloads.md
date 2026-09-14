# Exemplos de payloads — POST /forms

Exemplos completos prontos para copiar e adaptar. Substitua `<USER_ID>` pelo UUID do destinatário antes de enviar.

---

## Exemplo 1 — Formulário simples (1 section, 2 fields)

```json
{
  "form_title": "Vistoria Rápida",
  "user_id": "<USER_ID>",
  "system": "GAIA",
  "city": "São Paulo",
  "street": "Av. Paulista, 1000",
  "latitude": -23.56,
  "longitude": -46.65,
  "priority": 1,
  "justifications": [
    {"option": "Vistoria rotineira", "required_image": false, "required_text": false}
  ],
  "sections": [
    {
      "section_id": 1,
      "fields": [
        {"field_type": "TEXT_FIELD", "label": "Observação", "required": true, "key": "obs", "order": 1},
        {"field_type": "FILE_FIELD", "label": "Foto do local", "required": true, "key": "foto", "order": 2,
         "file_type": "IMAGE", "min_quantity": 1, "max_quantity": 5}
      ]
    }
  ]
}
```

---

## Exemplo 2 — Formulário médio (3 sections, mix de tipos)

```json
{
  "form_title": "Inspeção Predial Completa",
  "user_id": "<USER_ID>",
  "system": "GAIA",
  "city": "São Paulo",
  "street": "Av. Faria Lima, 2000",
  "latitude": -23.5734,
  "longitude": -46.6862,
  "priority": 2,
  "justifications": [
    {"option": "Vistoria programada", "required_image": false, "required_text": false},
    {"option": "Reclamação de morador", "required_image": true, "required_text": true}
  ],
  "sections": [
    {
      "section_id": 1,
      "fields": [
        {"field_type": "TEXT_FIELD", "label": "Nome do edifício", "required": true, "key": "nome_edificio", "order": 1},
        {"field_type": "DATE_FIELD", "label": "Data da vistoria", "required": true, "key": "data", "order": 2},
        {"field_type": "FILE_FIELD", "label": "Foto da fachada", "required": true, "key": "fachada", "order": 3,
         "file_type": "IMAGE", "min_quantity": 1, "max_quantity": 3}
      ]
    },
    {
      "section_id": 2,
      "fields": [
        {"field_type": "DROPDOWN_FIELD", "label": "Tipo de imóvel", "required": true, "key": "tipo_imovel", "order": 1,
         "options": ["Residencial", "Comercial", "Misto"]},
        {"field_type": "NUMBER_FIELD", "label": "Andares", "required": true, "key": "andares", "order": 2, "decimal": false},
        {"field_type": "SWITCH_BUTTON_FIELD", "label": "Acessibilidade adequada", "required": true, "key": "acessibilidade", "order": 3}
      ]
    },
    {
      "section_id": 3,
      "fields": [
        {"field_type": "RADIO_GROUP_FIELD", "label": "Estado de conservação", "required": true, "key": "estado", "order": 1,
         "options": ["Ótimo", "Bom", "Regular", "Ruim"]},
        {"field_type": "TEXT_FIELD", "label": "Parecer final", "required": true, "key": "parecer", "order": 2},
        {"field_type": "FILE_FIELD", "label": "Relatório técnico", "required": false, "key": "relatorio", "order": 3,
         "file_type": "DOCUMENT", "min_quantity": 0, "max_quantity": 2}
      ]
    }
  ]
}
```

---

## Exemplo 3 — Formulário com `information_fields`

`information_fields` aparecem no cabeçalho do formulário (não preenchidos pelo usuário).

```json
{
  "form_title": "Coleta com Localização",
  "user_id": "<USER_ID>",
  "system": "SGC",
  "city": "Campinas",
  "street": "Rua das Flores, 50",
  "latitude": -22.91,
  "longitude": -47.06,
  "priority": 1,
  "observation": "Ponto pré-cadastrado no sistema",
  "justifications": [
    {"option": "Coleta agendada", "required_image": false, "required_text": false}
  ],
  "information_fields": [
    {"information_field_type": "TEXT_INFORMATION_FIELD", "value": "Código do ponto: 8421-A"},
    {"information_field_type": "MAP_INFORMATION_FIELD", "latitude": -22.91, "longitude": -47.06}
  ],
  "sections": [
    {
      "section_id": 1,
      "fields": [
        {"field_type": "CHECKBOX_GROUP_FIELD", "label": "Materiais coletados", "required": true, "key": "materiais", "order": 1,
         "options": ["Papel", "Plástico", "Vidro", "Metal"]},
        {"field_type": "FILE_FIELD", "label": "Foto da coleta", "required": true, "key": "foto_coleta", "order": 2,
         "file_type": "IMAGE", "min_quantity": 1, "max_quantity": 4}
      ]
    }
  ]
}
```

---

## Exemplo 4 — Formulário no pool (`possession=OPEN`, sem dono)

Feature Uberlândia/SGISV (Fase 1). Repare que **não há campo `user_id`** — é omitido, não enviado como `null`. Token continua obrigatório (autentica a chamada e vira `created_by`).

```json
{
  "form_title": "Tapa-buraco - Av. Rondon Pacheco, 3500",
  "system": "GAIA",
  "city": "Uberlândia",
  "street": "Av. Rondon Pacheco, 3500",
  "latitude": -18.9146,
  "longitude": -48.2754,
  "priority": 1,
  "justifications": [
    {"option": "Buraco na via", "required_image": true, "required_text": false}
  ],
  "sections": [
    {
      "section_id": 1,
      "fields": [
        {"field_type": "TEXT_FIELD", "label": "Descrição da ocorrência", "required": true, "key": "descricao", "order": 1}
      ]
    }
  ]
}
```

Se a API responder `400 "Parâmetro ausente: user_id"`, o `system` usado ainda não tem `SystemConfig.allow_unassigned_forms=True` em `dev`/`homolog`. Siga o fallback da seção "Criar no pool" do `SKILL.md`: crie o mesmo payload **com** `user_id` = `sub` do token, e então chame:

```bash
curl -s -w "\nHTTP:%{http_code}\n" -X POST "$BASE/forms/<FORM_ID>/release" \
  -H "Authorization: Bearer $TOKEN"
```

O form volta pro pool (`possession=OPEN`) do mesmo jeito.

---

## Template de comando bash

Para criar vários forms em sequência, use este padrão (substitua o JSON entre as aspas simples):

```bash
export TOKEN="<bearer_jwt>"
export BASE="https://kuoea48f89.execute-api.sa-east-1.amazonaws.com/prod/mss-formularios"   # dev
# export BASE="https://ggbkn1e8p9.execute-api.sa-east-1.amazonaws.com/prod/mss-formularios"  # homolog

curl -s -w "\nHTTP:%{http_code}\n" -X POST "$BASE/forms" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{...payload aqui...}'
```

Para múltiplos forms, basta repetir o `curl` em sequência no mesmo bloco bash.
