#include <cs50.h>
#include <stdio.h>

void checksum(long n);

int sumOdds = 0;
int sumEven = 0;
int pos = 1;
int rem = 0;
int sum = 0;
long a = 100000000000000;
long cart = 0;

int main(void)
{
    long card = get_long("CARD: ");
    checksum(card);


}

// Funcao para fazer a soma dos valores
void checksum(long n)
{
    cart = n;
    while (cart > 0)
    {
        // Pegar o ultimo digito do cartao, eliminar ele e remover o ultimo digito no cartao
        rem = cart % 10;
        cart /= 10;

        if (pos % 2 == 0)
        {
            pos++;
            // Operacao de Multiplicar por 2
            rem *= 2;
            // Se for a multiplicacao for maior do que 10, separa e soma os dois digitos
            if (rem >= 10)
            {
                sumEven += rem % 10;
                sumEven += rem / 10;
            }

            else
            {
                sumEven += rem;
            }

        }

        else
        {
            // Somar os outros
            sumOdds += rem;
            pos++;
        }



    }
    // Verificacao Luhn's Algoritmo
    sum = sumOdds + sumEven;
    if (sum % 10 == 0)
    {
        // Verificar qual cartao, se a ultima posicao foi 17, pode ser Mastercard ou Visa, 16 AMEX, 14 VISA
        if (pos == 17)
        {
            if (n / 1000000000000000 == 4)
            {
                // Se começa com o digito 4, é VISA
                printf("VISA\n");
            }
            else if ((n / a == 51) || (n / a == 52) || (n / a == 53) || (n / a == 54) || (n / a == 55))
            {
                // Se comeca com 51,52,53,54 ou 55 é Mastercard
                printf("MASTERCARD\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if (pos == 14)
        {
            if (n / 1000000000000 == 4)
            {
                // Se começa com o digito 4, é VISA
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if (pos == 16)
        {
            if ((n / 10000000000000 == 34) || (n / 10000000000000 == 37))
            {
            printf("AMEX\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else
        {
            printf("INVALID\n");
        }

        //printf("VALID\n");
        //printf("%i\n",pos);
        //printf("%li\n",n/a);
        //printf("%li\n",n);
    }
    else
    {
        printf("INVALID\n");
    }
}