#include <stdio.h>
#include <mpi.h>

int main(int argc, char *argv[]) {
    int rank, size;

    MPI_Init(&argc, &argv); // Inicializa MPI
    MPI_Comm_size(MPI_COMM_WORLD, &size); // Número total de processos
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); // ID do processo atual

    printf("Olá do processo %d de %d\n", rank, size);

    MPI_Finalize(); // Finaliza MPI
    return 0;
}
/* Relato de Caso - Renan
A instalação foi de rápida aprendizagem e intuitiva, o que facilitou a familiarização com esta ferramenta.
Fiz testes usando vários núcleos de processador, um total de 9. Estes testes permitiram observar na prática o comportamento
da clusterização acontece nos processos. */
