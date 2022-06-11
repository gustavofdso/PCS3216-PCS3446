            @       /00
            JP      INICIO
VALOR1      K       =50         ; valor 1 a somar
VALOR2      K       #101101     ; valor 2 a somar
INICIO      LD      VALOR1      ; passando as variáveis
            +       VALOR2
            MM      GUARDAR
            HM      /00
GUARDAR     $       =1          ; endereco a ser guardado