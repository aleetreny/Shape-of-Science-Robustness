#include <stdint.h>
#include <stdlib.h>
#include <string.h>
/* Exact restriction of a fully sorted candidate order. No approximation. */
int filter_rankings(const int32_t *ranks, const int32_t *selections, const int32_t *ids,
                    int n, int repeats, int q, int k, int32_t *out) {
    unsigned char *mask=calloc((size_t)n,1); if(!mask) return 1;
    for(int r=0;r<repeats;r++) {
        memset(mask,0,(size_t)n);
        for(int j=0;j<q;j++) mask[selections[r*q+j]]=1;
        for(int j=0;j<q;j++) {
            int query=selections[r*q+j], got=0;
            for(int a=0;a<n && got<k;a++) {
                int pos=ranks[(size_t)query*n+a];
                if(mask[pos] && pos!=query) out[((size_t)r*q+j)*k+got++]=ids[pos];
            }
            if(got!=k) {free(mask);return 2;}
        }
    }
    free(mask); return 0;
}
/* All IDs are global row indices; flags avoid quadratic set intersections. */
int overlap_sums(const int32_t *neighbors, int variants, int q, int stride,
                 const int32_t *left, const int32_t *right, int pairs,
                 const int32_t *ks, int nk, int max_id, double *out) {
    int32_t *mark=calloc((size_t)max_id,sizeof(int32_t));if(!mark)return 1;
    int stamp=0;
    for(int p=0;p<pairs;p++) {
        if(left[p]>=variants || right[p]>=variants){free(mark);return 2;}
        for(int z=0;z<nk;z++) {
            int k=ks[z];long long sum=0;
            for(int i=0;i<q;i++) {
                ++stamp;
                const int32_t *a=neighbors+((size_t)left[p]*q+i)*stride;
                const int32_t *b=neighbors+((size_t)right[p]*q+i)*stride;
                for(int j=0;j<k;j++){if(a[j]<0 || a[j]>=max_id){free(mark);return 3;} mark[a[j]]=stamp;}
                for(int j=0;j<k;j++){if(b[j]<0 || b[j]>=max_id){free(mark);return 3;} sum+=(mark[b[j]]==stamp);}
            }
            out[p*nk+z]=(double)sum/(q*k);
        }
    }
    free(mark);return 0;
}
