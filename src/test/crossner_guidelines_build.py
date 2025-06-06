import json
from tqdm import tqdm
from pprint import pprint
from os import path, listdir

class Builder:
    def __init__(self, model_name: str, chunk_size=512, top_k=20, top_n=4, device='cuda:0') -> None:
        self._model_name = model_name
        self._ec_dir = path.join(path.dirname(path.dirname(path.dirname(__file__))), 'data', 'test', 'crossner-ec', self._model_name)
        self._final_dir = path.join(path.dirname(path.dirname(path.dirname(__file__))), 'data', 'test', 'crossner-rc', self._model_name)
        self._chunk_size = chunk_size
        self._top_n = top_n
        with open(path.join(self._ec_dir, 'cross.ec.json'), 'r') as f:
            self._raws = json.load(f)

        self._predicts = []
        with open(path.join(self._final_dir, 'cross.original.jsonl'), 'r') as f:
            line = f.readline()
            while line:
                self._predicts.append(json.loads(line.strip()))
                line = f.readline()

        self._prompts = {}
        prompts_dir = path.join(path.dirname(path.dirname(path.dirname(__file__))), 'data', 'database', 'crossner', 'prompts', self._model_name, 'guidelines')
        for prompt in listdir(prompts_dir):
            with open(path.join(prompts_dir, prompt), 'r') as f:
                self._prompts[prompt.split('.')[0]] = f.read()


    def build(self) -> int:
        saves = []
        pre_id = self._raws[0]['id']
        pre_entities = {}
        pre_source = self._raws[0]['source'].split('_')[0]
        pre_input = json.loads(self._raws[0]['instruction'])['input']
        count = 0
        size = len(self._raws)
        show = True
        for raw, predict in tqdm(zip(self._raws, self._predicts), total=size):
            assert predict['label'] == raw['output']
            count += 1
            id = raw['id']
            source = raw['source'].split('_')[0]
            instruction = json.loads(raw['instruction'])
            input = instruction['input']
            try:
                pd = json.loads(predict['predict'])
            except Exception as e:
                continue
            if pre_id != id or count >= size:
                for entity, types in pre_entities.items():
                    prompt = self._prompts[pre_source].format(
                        text=pre_input,
                        entity=entity)
                    saves.append({
                        'id': pre_id,
                        'source': pre_source,
                        'entity': entity,
                        'types': types,
                        'input': pre_input,
                        'instruction': prompt,
                        'output': pre_id
                    })
                    if show:
                        pprint(saves[0])
                        show = False
                pre_id = id
                pre_entities = {}
                pre_source = source
                pre_input = input
            for key, value in pd.items():
                for entity in value:
                    types = pre_entities.get(entity, [])
                    types.append(key)
                    pre_entities[entity] = types
        with open(path.join(self._final_dir, f'cross.rc.guidelines.json'), 'w') as f:
            json.dump(saves, f, indent=1)
        return len(saves)