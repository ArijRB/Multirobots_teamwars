/* drawn from pygame 1.9.2 files mask.h and bitmask.h */

#define BITMASK_W unsigned long int
#define BITMASK_W_LEN (sizeof(BITMASK_W)*CHAR_BIT)
#define BITMASK_W_MASK (BITMASK_W_LEN - 1)
#define BITMASK_N(n) ((BITMASK_W)1 << (n))

typedef struct bitmask
{
  int w,h;
  BITMASK_W bits[1];
} bitmask_t;


typedef struct {
  PyObject_HEAD
  bitmask_t *mask;
} PyMaskObject;



static int bitmask_getbit(const bitmask_t *m, int x, int y)
{
  return (m->bits[x/BITMASK_W_LEN*m->h + y] & BITMASK_N(x & BITMASK_W_MASK)) != 0;
}
