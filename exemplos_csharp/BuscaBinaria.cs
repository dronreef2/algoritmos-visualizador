// Exemplo: Busca Binária em C# (opcional)
// Apenas se você quiser explorar múltiplas linguagens

using System;

namespace Algoritmos
{
    public class BuscaBinaria
    {
        /// <summary>
        /// Busca binária básica em C#
        /// Complexidade: O(log n) tempo, O(1) espaço
        /// </summary>
        /// <param name="arr">Array ordenado</param>
        /// <param name="target">Elemento a buscar</param>
        /// <returns>Índice do elemento ou -1 se não encontrado</returns>
        public static int BuscaBasica(int[] arr, int target)
        {
            if (arr == null || arr.Length == 0)
                return -1;

            int esquerda = 0;
            int direita = arr.Length - 1;

            while (esquerda <= direita)
            {
                int meio = esquerda + (direita - esquerda) / 2;

                if (arr[meio] == target)
                    return meio;
                else if (arr[meio] < target)
                    esquerda = meio + 1;
                else
                    direita = meio - 1;
            }

            return -1;
        }

        // Método principal para teste
        public static void Main(string[] args)
        {
            int[] array = { 1, 3, 5, 7, 9, 11 };
            int target = 5;
            
            int resultado = BuscaBasica(array, target);
            Console.WriteLine($"Buscar {target} em [{string.Join(", ", array)}]: {resultado}");
            
            // Teste com elemento não encontrado
            target = 6;
            resultado = BuscaBasica(array, target);
            Console.WriteLine($"Buscar {target} em [{string.Join(", ", array)}]: {resultado}");
        }
    }
}
