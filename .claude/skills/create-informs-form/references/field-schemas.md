# Field Schemas — MSS Formulários

Referência completa dos 10 tipos de campo suportados na criação de formulários. Para cada tipo, lista os campos obrigatórios extras (além dos comuns) e dá um exemplo válido.

## Campos comuns (todos os tipos)

```json
{
  "field_type": "<TIPO>",
  "label": "Texto exibido",
  "required": true,
  "key": "identificador_unico_na_section",
  "order": 1,
  "help_text": "Opcional"
}
```

A `key` precisa ser **única dentro da mesma section**. Pode repetir entre sections diferentes.

---

## TEXT_FIELD
Sem campos obrigatórios extras. Opcionais: `regex`, `formatting`, `max_length`.

```json
{"field_type": "TEXT_FIELD", "label": "Descrição", "required": true, "key": "desc", "order": 1}
```

## NUMBER_FIELD
**Obrigatório**: `decimal` (bool — true = aceita decimais, false = só inteiros)
Opcionais: `min_value`, `max_value`.

```json
{"field_type": "NUMBER_FIELD", "label": "Quantidade", "required": true, "key": "qtd", "order": 1, "decimal": false}
```

## DROPDOWN_FIELD
**Obrigatório**: `options` (array de strings)

```json
{"field_type": "DROPDOWN_FIELD", "label": "Tipo", "required": true, "key": "tipo", "order": 1,
 "options": ["Opção A", "Opção B", "Opção C"]}
```

## TYPEAHEAD_FIELD
**Obrigatório**: `options` (array de strings)
Opcional: `max_length`.

```json
{"field_type": "TYPEAHEAD_FIELD", "label": "Categoria", "required": true, "key": "categoria", "order": 1,
 "options": ["Alfa", "Beta", "Gama"]}
```

## RADIO_GROUP_FIELD
**Obrigatório**: `options` (array de strings)

```json
{"field_type": "RADIO_GROUP_FIELD", "label": "Gravidade", "required": true, "key": "gravidade", "order": 1,
 "options": ["Baixa", "Média", "Alta"]}
```

## DATE_FIELD
Sem campos obrigatórios extras. Opcionais: `min_date`, `max_date` (timestamps em ms).

```json
{"field_type": "DATE_FIELD", "label": "Data", "required": true, "key": "data", "order": 1}
```

## CHECKBOX_FIELD
Sem campos obrigatórios extras. Representa um checkbox único (booleano).

```json
{"field_type": "CHECKBOX_FIELD", "label": "Confirma os dados", "required": true, "key": "confirma", "order": 1}
```

## CHECKBOX_GROUP_FIELD
**Obrigatório**: `options` (array de strings)
Opcional: `check_limit` (int — máximo de opções selecionáveis)

```json
{"field_type": "CHECKBOX_GROUP_FIELD", "label": "Itens encontrados", "required": false, "key": "itens", "order": 1,
 "options": ["Vidro quebrado", "Porta danificada", "Goteira"], "check_limit": 2}
```

## SWITCH_BUTTON_FIELD
Sem campos obrigatórios extras. Toggle on/off (booleano).

```json
{"field_type": "SWITCH_BUTTON_FIELD", "label": "Ativo", "required": true, "key": "ativo", "order": 1}
```

## FILE_FIELD
**Obrigatórios (3)**: `file_type` (`IMAGE` | `DOCUMENT`), `min_quantity` (int), `max_quantity` (int)

```json
{"field_type": "FILE_FIELD", "label": "Foto do local", "required": true, "key": "foto", "order": 1,
 "file_type": "IMAGE", "min_quantity": 1, "max_quantity": 5}
```

`min_quantity: 0` torna o upload opcional mesmo com `required: true` no contexto da section (quando combinado com `required: false`, é totalmente opcional).

---

## Information Fields (campos de cabeçalho do form)

`information_fields` é diferente de `sections.fields`. São informações fixas exibidas no topo do formulário (não preenchidas pelo usuário). Tipos suportados:

### TEXT_INFORMATION_FIELD
```json
{"information_field_type": "TEXT_INFORMATION_FIELD", "value": "Texto exibido"}
```

### MAP_INFORMATION_FIELD
```json
{"information_field_type": "MAP_INFORMATION_FIELD", "latitude": -23.56, "longitude": -46.65}
```

### FILE_INFORMATION_FIELD
Gera presigned URL para upload na criação.
```json
{"information_field_type": "FILE_INFORMATION_FIELD",
 "filename": "documento.pdf", "mimetype": "application/pdf", "file_type": "DOCUMENT"}
```

---

## Justification Options

`justifications` é um array de opções de cancelamento que o usuário pode escolher se for cancelar o formulário.

```json
{
  "option": "Texto da opção",
  "required_image": false,  // se true, exige imagem ao cancelar com essa opção
  "required_text": false    // se true, exige texto ao cancelar com essa opção
}
```

Pelo menos 1 opção é obrigatória.
