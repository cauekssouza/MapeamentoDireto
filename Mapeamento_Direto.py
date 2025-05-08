import time

class CacheMapeamentoDireto:
    def __init__(self, tamanho_ram=256, tamanho_cache=8, tamanho_bloco=4):
        self.ram = {i: 0 for i in range(tamanho_ram)} 
        self.cache = [
            {
                'tag': None,
                'dados': [0] * tamanho_bloco,
                'valido': False,
                'sujo': False
            } for _ in range(tamanho_cache)
        ]
        self.tamanho_bloco = tamanho_bloco
        self.acessos = {'hit': 0, 'miss': 0}
        self.tamanho_ram = tamanho_ram

    def exibir_ram(self):
        print("\nConteúdo da RAM:")
        for endereco, valor in self.ram.items():
            print(f"Endereço {endereco}: {valor}")

    def exibir_cache(self):
        print("\nEstado da Cache:")
        for i, linha in enumerate(self.cache):
            status = f"Tag {linha['tag']} {'(suja)' if linha['sujo'] else ''}"
            print(f"Linha {i}: {status} | Dados: {linha['dados']} | Válido: {linha['valido']}")
        time.sleep(0.5)  

    def calculo_indice_tag_offset(self, endereco):
        num_linhas = len(self.cache)
        bloco = endereco // self.tamanho_bloco
        indice = bloco % num_linhas
        tag = bloco // num_linhas
        offset = endereco % self.tamanho_bloco
        return indice, tag, offset

    def busca(self, endereco, novo_valor=None):
        if endereco < 0 or endereco >= self.tamanho_ram:
            raise ValueError(f"Endereço {endereco} está fora dos limites (0-{self.tamanho_ram - 1}).")

        indice, tag, offset = self.calculo_indice_tag_offset(endereco)
        linha = self.cache[indice]

        
        if linha['valido'] and linha['tag'] == tag:
            self.acessos['hit'] += 1
            print(f"Cache hit! Endereço {endereco}")

            if novo_valor is not None:
                linha['dados'][offset] = novo_valor
                linha['sujo'] = True
            return linha['dados'][offset]

        
        self.acessos['miss'] += 1
        print(f"Cache miss! Endereço {endereco}")

        self.atualizando_cache(indice, tag, endereco)

        if novo_valor is not None:
            self.ram[endereco] = novo_valor
            self.cache[indice]['dados'][offset] = novo_valor
            self.cache[indice]['sujo'] = True

        return self.ram.get(endereco, 0)

    def atualizando_cache(self, indice, tag, endereco):
       
        if self.cache[indice]['sujo']:
            bloco_base = self.cache[indice]['tag'] * len(self.cache) * self.tamanho_bloco
            for i in range(self.tamanho_bloco):
                if bloco_base + i < self.tamanho_ram:
                    self.ram[bloco_base + i] = self.cache[indice]['dados'][i]

       
        bloco_inicial = (endereco // self.tamanho_bloco) * self.tamanho_bloco
        dados_bloco = [self.ram.get(i, 0) for i in range(bloco_inicial, bloco_inicial + self.tamanho_bloco) if i < self.tamanho_ram]

        self.cache[indice] = {
            'tag': tag,
            'dados': dados_bloco,
            'valido': True,
            'sujo': False
        }



tamanho_ram = 16


tamanho_cache = 4
tamanho_bloco = 4
cache = CacheMapeamentoDireto(tamanho_ram, tamanho_cache, tamanho_bloco)


for i in range(tamanho_ram):
    cache.ram[i] = i * 10


cache.exibir_ram()
cache.exibir_cache()


cache.busca(5)  
cache.exibir_cache()

cache.busca(6)  
cache.exibir_cache()

cache.busca(5, novo_valor=999)  
cache.exibir_ram()
cache.exibir_cache()

try:
    cache.busca(16)  
except ValueError as e:
    print(e)


hit_rate = cache.acessos['hit'] / (cache.acessos['hit'] + cache.acessos['miss']) if (cache.acessos['hit'] + cache.acessos['miss']) > 0 else 0
print(f"Taxa de acertos: {hit_rate:.1%}")
