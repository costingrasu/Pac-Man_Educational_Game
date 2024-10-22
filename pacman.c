#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <conio.h>
#include <winsock2.h>
#include <windows.h>


#pragma comment(lib, "ws2_32.lib")

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 12345


typedef struct Node
{    
    int isPoint;
    struct Node *neighbors[4];
    int i;
    int j;
}Node;

typedef struct Graph
{
    Node *nodes[33][30];
}Graph;

// Function to create a new node
Node* create_node(int point) 
{
    Node *new_node = (Node*)malloc(sizeof(Node));
    if (new_node == NULL) 
    {
        printf("Memory allocation failed\n");
        exit(1);
    }

    new_node->isPoint = point;

    for (int i = 0; i < 4; i++) 
    {
        new_node->neighbors[i] = NULL;
    }
    return new_node;
}

void CreateG(Graph **g , int level[][30])
{
    for (int i = 0 ; i < 33 ; i++)
    {
        for (int j = 0 ; j < 30 ; j++)
        {
            if (level[i][j] == 0 || level[i][j] == 1 || level[i][j] == 2)
            {
                Node *nod;

                if (level[i][j] == 0)
                {
                    nod = create_node(0);
                    nod->i = i;
                    nod->j = j;
                    (*g)->nodes[i][j] = nod;
                }
                else if (level[i][j] == 1)
                {
                    nod = create_node(1);
                    nod->i = i;
                    nod->j = j;
                    (*g)->nodes[i][j] = nod;
                }
                else if (level[i][j] == 2)
                {
                    nod = create_node(2);
                    nod->i = i;
                    nod->j = j;
                    (*g)->nodes[i][j] = nod;
                }
            }
        }
    }

    for (int i = 0 ; i < 33 ; i++)
    {
        for (int j = 0 ; j < 30 ; j++)
        {
            if ((*g)->nodes[i][j] != NULL)
            {
                Node *nod = (*g)->nodes[i][j];

                if (i - 1 >= 0 && (level[i - 1][j] == 0 || level[i - 1][j] == 1 || level[i - 1][j] == 2))
                {
                    nod->neighbors[2] = (*g)->nodes[i - 1][j]; // Up
                }

                if (i + 1 <= 32 && (level[i + 1][j] == 0 || level[i + 1][j] == 1 || level[i + 1][j] == 2))
                {
                    nod->neighbors[3] = (*g)->nodes[i + 1][j]; // Down
                }

                if (j - 1 >= 0 && (level[i][j - 1] == 0 || level[i][j - 1] == 1 || level[i][j - 1] == 2))
                {
                    nod->neighbors[1] = (*g)->nodes[i][j - 1]; // Left
                }

                if (j + 1 <= 29 && (level[i][j + 1] == 0 || level[i][j + 1] == 1 || level[i][j + 1] == 2))
                {
                    nod->neighbors[0] = (*g)->nodes[i][j + 1]; // Right
                }
            }
        }
    }
}


//HANDLE mutex;

// DWORD WINAPI threadFunction(LPVOID lpParam){
//     char server_reply[1024];
//     int recv_size;

//     while (1) {
//         // Receive data from the server
//         if ((recv_size = recv(sock, server_reply, 1024, 0)) == SOCKET_ERROR) {
//             printf("recv failed\n");
//             break;
//         }
//         server_reply[recv_size] = '\0';
//         printf("primit: %s\n", server_reply);

//         // Parse the received string to extract the numbers
//         int new_lin, new_col;
//         if (sscanf(server_reply, "%d %d", &new_lin, &new_col) == 2) {
//             WaitForSingleObject(mutex, INFINITE);
//             lin = new_lin;
//             col = new_col;
//             ReleaseMutex(mutex);
//             printf("Parsed lin: %d, col: %d\n", lin, col);
//         } else {
//             printf("Failed to parse the numbers from the server reply\n");
//         }
//     }

//     return 0;

// }


int main(void)
{
    

    int level[33][30] = {
        {6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5},
        {3, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 3},
        {3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3},
        {3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3},
        {3, 3, 2, 3, 0, 0, 3, 1, 3, 0, 0, 0, 3, 1, 3, 3, 1, 3, 0, 0, 0, 3, 1, 3, 0, 0, 3, 2, 3, 3},
        {3, 3, 1, 7, 4, 4, 8, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 7, 4, 4, 8, 1, 3, 3},
        {3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3},
        {3, 3, 1, 6, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 5, 1, 3, 3},
        {3, 3, 1, 7, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 8, 1, 3, 3},
        {3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3},
        {3, 7, 4, 4, 4, 4, 5, 1, 3, 7, 4, 4, 5, 0, 3, 3, 0, 6, 4, 4, 8, 3, 1, 6, 4, 4, 4, 4, 8, 3},
        {3, 0, 0, 0, 0, 0, 3, 1, 3, 6, 4, 4, 8, 0, 7, 8, 0, 7, 4, 4, 5, 3, 1, 3, 0, 0, 0, 0, 0, 3},
        {3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3},
        {8, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 4, 4, 9, 9, 4, 4, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 7},
        {4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4},
        {0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0},
        {4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4},
        {5, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 7, 4, 4, 4, 4, 4, 4, 8, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 6},
        {3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3},
        {3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 4, 4, 4, 4, 4, 4, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3},
        {3, 6, 4, 4, 4, 4, 8, 1, 7, 8, 0, 7, 4, 4, 5, 6, 4, 4, 8, 0, 7, 8, 1, 7, 4, 4, 4, 4, 5, 3},
        {3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3},
        {3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3},
        {3, 3, 1, 7, 4, 5, 3, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 3, 6, 4, 8, 1, 3, 3},
        {3, 3, 2, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 2, 3, 3},
        {3, 7, 4, 5, 1, 3, 3, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 3, 3, 1, 6, 4, 8, 3},
        {3, 6, 4, 8, 1, 7, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 8, 1, 7, 4, 5, 3},
        {3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3},
        {3, 3, 1, 6, 4, 4, 4, 4, 8, 7, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 8, 7, 4, 4, 4, 4, 5, 1, 3, 3},
        {3, 3, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 3, 3},
        {3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3},
        {3, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 3},
        {7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8}
        };
    
    
    Graph *g = malloc(sizeof(Graph));

    for ( int i = 0; i < 33 ; i++){
            for ( int j = 0; j < 30 ; j++){
                g->nodes[i][j] = NULL;
            }
    }

    CreateG(&g , level);

    //PT INT THREAD
    // HANDLE inputThread;
    // DWORD inputThreadIds;
    // int inputThreadArgs;

    WSADATA wsa;
    SOCKET sock;
   
    struct sockaddr_in server;
    char message[1024];
   
    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        printf("WSAStartup failed. Error Code : %d", WSAGetLastError());
        return 1;
    }

    // Create socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        printf("Could not create socket : %d", WSAGetLastError());
        return 1;
    }

    server.sin_addr.s_addr = inet_addr(SERVER_IP);
    server.sin_family = AF_INET;
    server.sin_port = htons(SERVER_PORT);

    // Connect to server
    if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0) {
        printf("Connect failed. Error");
        return 1;
    }
    else {
        printf(" Connection good");
    }

    
    Node *pac = NULL;

    int intrb = 0;

    // mutex = CreateMutex(NULL, FALSE, NULL);
    // if (mutex == NULL) {
    //     printf("CreateMutex error: %d\n", GetLastError());
    //     return 1;
    // }



    //THREAD INPUT
    //     inputThread = CreateThread(
    //     NULL,              // Default security attributes
    //     0,                 // Default stack size
    //     threadFunction,    // Thread function
    //     NULL,    // Argument to thread function
    //     0,                 // Default creation flags
    //     &inputThreadIds      // Pointer to receive the thread ID
    //     );

    //     if (inputThread == NULL) {
    //         fprintf(stderr, "Error creating thread\n");
    //         return 1;
    //     }
    // printf("Ajunge aici macar5");
    int lin,col;
    while (true)
    {   
        if (recv(sock, message, sizeof(message), 0) < 0) {
            printf("Receive failed\n");
            
        }

        // Parse lin and col from message (assuming message format is "lin col")
        sscanf(message, "%d %d", &lin, &col);
        
        // Process lin and col as needed
        printf("Received lin=%d col=%d\n", lin, col);
        lin = 2;
        col = 2;
        if(col != 30)
            col = 2;
        printf("\n%d",lin);
        if (pac == NULL)
            pac = g->nodes[lin][col];
        else
        {
            if (lin > pac->i)
            {
                pac = pac->neighbors[3];
            }

            if (lin < pac->i)
            {
                pac = pac->neighbors[2];
            }

            if (col > pac->j)
            {
                pac = pac->neighbors[0];
            }

            if (col < pac->j)
            {
                pac = pac->neighbors[1];
            }

        }
      
        if (pac ->isPoint == 2)
        {
            intrb++;
            sprintf(message, "%d", intrb);
            if (send(sock, message, strlen(message), 0) < 0) {
                printf("Send failed");
                
            }
        }
        
        Sleep(16);
       
    }
    
    closesocket(sock);
    WSACleanup();
    return 0;
}