; Soma
; *********
; Programa principal que chama o somador.

SOMADOR     <                       ; cabeçalho - definindo entry-points
ENTRADA1    <
ENTRADA2    <
SAIDA       >

            @       /0000           ; endereço inicial do código na memória
            JP      INICIO
VALOR1      K       =50             ; valor 1 a somar
VALOR2      K       #101101         ; valor 2 a somar
SAIDA       K       /0000           ; endereço de salvamento da soma
INICIO      LD      VALOR1          ; passando as variáveis na memória
            MM      ENTRADA1
            LD      VALOR2
            MM      ENTRADA2
            SC      SOMADOR         ; chamando o somador
            PD      =0              ; exibindo dados na tela
            #                       ; fim do programa