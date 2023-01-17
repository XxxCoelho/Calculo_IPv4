import re


class CalculoIpv4:
    def __init__(self, ip, mascara=None, prefixo=None):
        self.ip = ip
        self.prefixo = prefixo
        self.mascara = mascara

        if mascara is None and prefixo is None:
            raise ValueError('Precisa enviar uma mascara ou prefixo!')

        if mascara and prefixo:
            raise ValueError('Precisa enviar uma mascara ou prefixo, não ambos!')

        self._conj_rede()
        self._conj_broadcast()

    @property
    def ip(self):
        return self._ip

    @property
    def mascara(self):
        return self._mascara

    @property
    def prefixo(self):
        if self._prefixo is None:
            return
        return self._prefixo

    @property
    def numero_IPS(self):
        return self.pegar_ips()

    @property
    def rede(self):
        return self._rede

    @property
    def broadcast(self):
        return self._broadcast

    @ip.setter
    def ip(self, valor):
        if not self.valida_ip(valor):
            raise ValueError('Ip invalido!')

        self._ip = valor
        self._ip_bin = self.ip_para_bin(valor)

    @mascara.setter
    def mascara(self, valor):
        if not valor:
            return
        if not self.valida_ip(valor):
            raise ValueError('Mascara invalida')

        self._mascara = valor
        self._mascara_bin = self.ip_para_bin(valor)

        if not hasattr(self, 'prefixo'):
            self.prefixo = self._mascara_bin.count('1')

    @prefixo.setter
    def prefixo(self, valor):
        if valor is None:
            return

        try:
            valor = int(valor)
        except ValueError:
            raise 'Prefixo deve ser um valor inteiro'

        if valor > 32 or valor < 0:
            raise TypeError('Prefixo precisa ter 32 Bits')

        self._prefixo = valor
        self._mascara_bin = (valor * '1').ljust(32, '0')

        if not hasattr(self, 'mascara'):
            self.mascara = self.bin_para_ip(self._mascara_bin)

    @staticmethod
    def valida_ip(ip):
        ip_regexp = re.compile(r"^(?:[0-9]{1,3}.){3}[0-9]{1,3}$", )

        if ip_regexp.search(ip):
            return True

    @staticmethod
    def ip_para_bin(ip):
        bloco = ip.split('.')
        bloco_bin = [str(bin(int(n)))[2:].zfill(8) for n in bloco]
        bloco_str_bin = ''.join(bloco_bin)
        quantidade_bits = len(bloco_str_bin)

        if quantidade_bits > 32:
            raise ValueError('IP ou mascara possui mais de 32 bits')

        return bloco_str_bin

    @staticmethod
    def bin_para_ip(ip):
        bit = 8
        bloco = [str(int(ip[i:bit + i], 2)) for i in range(0, 32, bit)]
        return '.'.join(bloco)

    def pegar_ips(self):
        return 2 ** (32 - self.prefixo)

    def _conj_rede(self):
        host_bits = 32 - self.prefixo
        self._rede_bin = self._ip_bin[:self.prefixo] + (host_bits * '0')
        self._rede = self.bin_para_ip(self._rede_bin)
        return self._rede

    def _conj_broadcast(self):
        host_bits = 32 - self.prefixo
        self._broad_bin = self._ip_bin[:self.prefixo] + (host_bits * '1')
        self._broadcast = self.bin_para_ip(self._broad_bin)
        return self._broadcast


ipv4 = CalculoIpv4(ip='192.168.0.250', mascara='255.255.255.192')
print(f'Prefixo: {ipv4.prefixo}')
print(f'Mascara: {ipv4.mascara}')
print(f'IP: {ipv4.ip}')
print(f'Numero de IPS da rede: {ipv4.numero_IPS}')
print(f'Rede: {ipv4.rede}')
print(f'BroadCast: {ipv4.broadcast}')
print('#' * 20)
ipv4_2 = CalculoIpv4(ip='122.144.232.250', prefixo=26)
print(f'Prefixo: {ipv4_2.prefixo}')
print(f'Mascara: {ipv4_2.mascara}')
print(f'IP: {ipv4_2.ip}')
print(f'Numero de IPS da rede: {ipv4_2.numero_IPS}')
print(f'Rede: {ipv4_2.rede}')
print(f'BroadCast: {ipv4_2.broadcast}')