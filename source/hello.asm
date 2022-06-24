            @       /0000           ; endereço inicial do código na memória
            JP      START

STRING      K       =72
            K       =101
            K       =108
            K       =108
            K       =111
            K       =44
            K       =32
            K       =119
            K       =111
            K       =114
            K       =108
            K       =100
            K       =33
            K       =0

ONE         K       =1
CURR        K       =2
ADD1        K       =0
ADD2        K       =0

START       LV      =0
            +       CURR
            MM      ADD2
            HM      /01
            LD      ADD1
            JZ      END
            PD      =3
            LD      CURR
            +       ONE
            MM      CURR
            JP      START

END         OS      /0F