# Instruction
You need to answer the **type** of the corresponding entity in the text according to the **Types** and **the relevant documents retrieved**.
# Text
{text}
# Entity
{entity}
# Relevant Documents
{documents}
# Types
['algorithm', 'conference', 'country', 'field', 'location', 'metrics', 'misc', 'organisation', 'person', 'product', 'programlang', 'researcher', 'task', 'university']
# Rules
1. If the entity may belong to more than one type, select the most specific type. For example, if a entity is both a researcher and a person, then it should be a researcher. And if a entity is both a country and a location, then it should be a country.
2. Your reply only needs to be output according to the format and no additional information is required.
# Answer format
{{"entity": "the entity in Entity","reason": "The reason you judge the type which from Types", "entity_type": "type from Types"}}