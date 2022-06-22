            @       /00         ; endereco 0x0 do banco 0
            JP      INICIO
VALOR1      K       =50         ; valor 1 a somar
VALOR2      K       =4          ; valor 2 a somar
SAIDA       $       =1          ; endereco a ser guardado
INICIO      LD      VALOR1      ; passando as variáveis
            +       VALOR2
            MM      SAIDA       ; salvando na memória
            OS      /00         ; exibindo os dados pelo OS
            #                   ; fim do programa