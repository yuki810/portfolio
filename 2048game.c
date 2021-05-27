#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void move(int arrow, const int height, const int width, int cell[height][width]);
void printcell(FILE *fp, int count, const int height, const int width, int cell[height][width]);
void numgenerate(const int height, const int width, int cell[height][width]);
int conditioncheck(const int height, const int width, int cell[height][width]);

int main(){
    /* 初期設定*/
    FILE *fp = stdout;
    const int height = 4;
    const int width = 4;
    int cell[height][width];
    for(int y = 0; y < height; ++y){
        for(int x = 0; x < width; ++x){
            cell[y][x] = 0;
        }
    }
    int empty[height][width];
    for(int y = 0; y < height; ++y){
        for(int x = 0; x < width; ++x){
            empty[y][x] = 0;
        }
    }
    int count = 0;

    /* 初期状態 */
    numgenerate(height, width, cell);
    numgenerate(height, width, cell);
    printcell(fp, count, height, width, cell);

    /*　2048ゲーム　*/
    system("/bin/stty raw onlcr");// enterを押さなくてもキー入力を受け付けるようになる
    int arrow;
    int breaknum = 0;
    while((arrow = getchar()) != '.'){
        if(arrow == 65 || arrow == 66 || arrow == 67 || arrow == 68){
            count += 1;
            move(arrow, height, width, cell);
            numgenerate(height, width, cell);
            fprintf(fp,"\e[%dA",height+1);//カーソルを上に戻す(表示部+説明文×2)
            fprintf(fp,"\e[0J");
            printcell(fp, count, height, width, cell);
            breaknum = conditioncheck(height, width, cell);
            if(breaknum == 1 || breaknum == 2){
                break;
            }
        }
    }
    system("/bin/stty cooked");

    /* GAMECLEARの時　*/
    if(breaknum == 1){
        printf("\e[35mCongratulations! You can complete 2048!\e[0m\r\n");
        printf("Your score is %d\r\n", count);
        printf("(smaller score is better)\r\n");
    }
    /* GAMEOVERの時　*/
    else if(breaknum == 2){
        printf("\e[31mGAME OVER!\e[0m\r\n");
        printf("Please try again.\r\n");
    }
}

/* 矢印入力をセルに反映する関数 */
void move(int arrow, const int height, const int width, int cell[height][width]){
    if(arrow == 65){//上矢印の時
        int upnum = 0;
        for(int x = 0; x < width; ++x){
            for(int y = 0; y< height; ++y){
                if(cell[y][x] == 0){
                    upnum += 1;
                }else if(cell[y][x] != 0){
                    if(upnum != 0){
                        cell[y-upnum][x] = cell[y][x];
                        cell[y][x] = 0;
                    }
                }
            }
            if(cell[0][x] == cell[1][x] && cell[2][x] == cell[3][x]){
                cell[0][x] = cell[0][x]*2;
                cell[1][x] = cell[2][x]*2;
                cell[2][x] = 0;
                cell[3][x] = 0;
            }else if(cell[0][x] == cell[1][x]){
                cell[0][x] = cell[0][x]*2;
                cell[1][x] = cell[2][x];
                cell[2][x] = cell[3][x];
                cell[3][x] = 0;
            }else if(cell[1][x] == cell[2][x]){
                cell[1][x] = cell[1][x]*2;
                cell[2][x] = cell[3][x];
                cell[3][x] = 0;
            }else if(cell[2][x] == cell[3][x]){
                cell[2][x] = cell[2][x]*2;
                cell[3][x] = 0;
            }
            upnum = 0;
        }
    }else if(arrow == 66){//下矢印の時
        int downnum = 0;
        for(int x = 0; x < width; ++x){
            for(int y = 0; y< height; ++y){
                if(cell[height - y - 1][x] == 0){
                    downnum += 1;
                }else if(cell[height - y - 1][x] != 0){
                    if(downnum != 0){
                        cell[height - y - 1 + downnum][x] = cell[height - y - 1][x];
                        cell[height - y - 1][x] = 0;
                    }
                }
            }
            if(cell[3][x] == cell[2][x] && cell[1][x] == cell[0][x]){
                cell[3][x] = cell[3][x]*2;
                cell[2][x] = cell[1][x]*2;
                cell[1][x] = 0;
                cell[0][x] = 0;
            }else if(cell[3][x] == cell[2][x]){
                cell[3][x] = cell[3][x]*2;
                cell[2][x] = cell[1][x];
                cell[1][x] = cell[0][x];
                cell[0][x] = 0;
            }else if(cell[2][x] == cell[1][x]){
                cell[2][x] = cell[2][x]*2;
                cell[1][x] = cell[0][x];
                cell[0][x] = 0;
            }else if(cell[1][x] == cell[0][x]){
                cell[1][x] = cell[1][x]*2;
                cell[0][x] = 0;
            }
            downnum = 0;
        }
    } else if(arrow == 67){//右矢印の時
        int rightnum = 0;
        for(int y = 0; y < height; ++y){
            for(int x = 0; x < width; ++x){
                if(cell[y][width - x - 1] == 0){
                    rightnum += 1;
                }else if(cell[y][width - x -1] != 0){
                    if(rightnum != 0){
                        cell[y][width - x - 1 + rightnum] = cell[y][width - x - 1];
                        cell[y][width - x - 1] = 0;
                    }
                }
            }
            if(cell[y][3] == cell[y][2] && cell[y][1] == cell[y][0]){
                cell[y][3] = cell[y][3]*2;
                cell[y][2] = cell[y][1]*2;
                cell[y][1] = 0;
                cell[y][0] = 0;
            }else if(cell[y][3] == cell[y][2]){
                cell[y][3] = cell[y][3]*2;
                cell[y][2] = cell[y][1];
                cell[y][1] = cell[y][0];
                cell[y][0] = 0;
            }else if(cell[y][2] == cell[y][1]){
                cell[y][2] = cell[y][2]*2;
                cell[y][1] = cell[y][0];
                cell[y][0] = 0;
            }else if(cell[y][1] == cell[y][0]){
                cell[y][1] = cell[y][1]*2;
                cell[y][0] = 0;
            }
            rightnum = 0;
        }
    }else if(arrow == 68){//左矢印の時
        int leftnum = 0;
        for(int y = 0; y < width; ++y){
            for(int x = 0; x < width; ++x){
                if(cell[y][x] == 0){
                    leftnum += 1;
                }else if(cell[y][x] != 0){
                    if(leftnum != 0){
                        cell[y][x-leftnum] = cell[y][x];
                        cell[y][x] = 0;
                    }
                }
            }
            if(cell[y][0] == cell[y][1] && cell[y][2] == cell[y][3]){
                cell[y][0] = cell[y][0]*2;
                cell[y][1] = cell[y][2]*2;
                cell[y][2] = 0;
                cell[y][3] = 0;
            }else if(cell[y][0] == cell[y][1]){
                cell[y][0] = cell[y][0]*2;
                cell[y][1] = cell[y][2];
                cell[y][2] = cell[y][3];
                cell[y][3] = 0;
            }else if(cell[y][1] == cell[y][2]){
                cell[y][1] = cell[y][1]*2;
                cell[y][2] = cell[y][3];
                cell[y][3] = 0;
            }else if(cell[y][2] == cell[y][3]){
                cell[y][2] = cell[y][2]*2;
                cell[y][3] = 0;
            }
            leftnum = 0;
        }

    }
}

/* ゲーム画面の表示 */
void printcell(FILE *fp, int count, const int height, const int width, int cell[height][width]){
    fprintf(fp, "count = %d\r\n", count);
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            // ANSIエスケープコードを用いて、色付きの数字を表示
            // \e[0m でリセット（リセットしないと以降も赤くなる）
            if(cell[y][x]){
                fprintf(fp, "\e\e[38;5;%dm%d\t\e[0m",30 + cell[y][x]*3, cell[y][x]);
            }
            else{
	            fprintf(fp, "-\t");
            }
        }
        fprintf(fp,"\r\n");
    }
    fflush(fp);
}

/* ランダムに数字を発生させる　*/
void numgenerate(const int height, const int width, int cell[height][width]){
    int buf[16][2];
    int count = 0;
    for(int y = 0; y < height; ++y){
        for(int x = 0; x < width; ++x){
            if(cell[y][x] == 0){
                buf[count][0] = y;
                buf[count][1] = x;
                count += 1;
            }
        }
    }
    if(count != 0){
        srand((unsigned int)time(NULL));
        int random = rand() % count;
        double pro = (double)rand()/RAND_MAX;
        if(pro < 0.1){
            cell[buf[random][0]][buf[random][1]] = 4;
        }else{
        cell[buf[random][0]][buf[random][1]] = 2;
        }
    }
}

/* ゲーム継続確認 */
int conditioncheck(const int height, const int width, int cell[height][width]){
    for(int y = 0; y < height; y++){
        for(int x = 0; x < width; ++x){
            if(cell[y][x] == 2048){
                return 1;
            }else if(cell[y][x] == 0){
                return 0;
            }
        }
    }
    if(cell[0][0] == cell[0][1] || cell[0][0] == cell[1][0]){
        return 0;
    }else if(cell[height-1][width-1] == cell[height-2][width-1] || cell[height-1][width-1] == cell[height-1][width-2]){
        return 0;
    }else if(cell[0][width-1] == cell[0][width-2] || cell[0][width-1] == cell[1][width-1]){
        return 0;
    }else if(cell[height-1][0] == cell[height-2][0] || cell[height-1][0] == cell[height-1][1]){
        return 0;
    }else if(cell[1][0] == cell[2][0] || cell[1][width-1] == cell[2][width - 1] || cell[0][1] == cell[0][2] || cell[height-1][1] == cell[height-1][2]){
        return 0;
    }else{
        for(int y =1; y < height-1; ++y){
            for(int x = 1; x < width-1; ++x){
                if(cell[y][x] == cell[y-1][x] || cell[y][x] == cell[y+1][x] || cell[y][x] == cell[y][x-1] || cell[y][x] == cell[y][x+1]){
                    return 0;
                }
            }
        }
    }
    return 2;
}