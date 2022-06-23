SOMADOR     <
ENTRADA1    <
ENTRADA2    <
SAIDA       >

            @       /0000
            JP      INICIO
VALOR1      K       =50
VALOR2      K       =60
SAIDA       K       /0000
INICIO      LD      VALOR1
            MM      ENTRADA1
            LD      VALOR2
            MM      ENTRADA2
            SC      SOMADOR
            PD      =3
            HM      /00