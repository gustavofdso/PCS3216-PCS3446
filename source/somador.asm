; Somador
; *********
; Subrotina que realiza uma soma de dois valores na memória, e deposita o resultado no acumulador.

SOMADOR     >                       ; cabeçalho - definindo entry-points
ENTRADA1    >
ENTRADA2    >

            @       /00FF           ; endereço inicial do código na memória
            JP      SOMADOR
ENTRADA1    K       =0              ; valor 1 a somar
ENTRADA2    K       =0              ; valor 2 a somar
SOMADOR     LD      ENTRADA1        ; realizando a soma
            +       ENTRADA2
            RS                      ; retornando da sub-rotina