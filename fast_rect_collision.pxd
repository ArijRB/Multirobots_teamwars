#cython: boundscheck=False, nonecheck=False,initializedcheck=False,cdivision=True

import cython

####################################################


cdef class cyRectSprite:
    cdef int top,left,right,bottom
    cdef long spriteid
    cdef object sprite
    cdef object layername

    @cython.locals(h=cython.int,w=cython.int)
    cdef int size(self)

    @cython.locals(maxspritesize=cython.int,screensize=cython.int)
    cdef bint well_formed(self,maxspritesize,screensize)

  ####################################################

cdef class FastGroupCollide:
    cdef int max_interval
    cdef int display_size
    cdef int array_size
    cdef dict ref
    cdef list [:,::1] array

    @cython.locals(cys=cyRectSprite,i=cython.int,j=cython.int)
    cdef list _get_list(self,cys)

    @cython.locals(cys=cyRectSprite,l=cython.list)
    cdef _unsafe_add_cyRectSprite(self,cys,l)

    @cython.locals(cys=cyRectSprite,l=cython.list)
    cdef _add_cyRectSprite(self,cys,l=*)

    @cython.locals(ref=cython.dict,id_s=cython.long,l=cython.list,k=cython.int,last=cyRectSprite)
    cpdef remove_sprite(self,s)

    @cython.locals(old_l=cython.list,new_l=cython.list,cys=cyRectSprite,id_s=cython.long)
    cpdef add_or_update_sprite(self,s)

    @cython.locals(l=cython.int,t=cython.int,r=cython.int,b=cython.int,     \
                    i=cython.int,j=cython.int,id_s=cython.long,di=cython.int,dj=cython.int, \
                    lst2=cython.list,s2=cyRectSprite,candidates=cython.list,gFilter=cython.set)
    cdef _compute_collision_list(self,l,t,r,b,s=*,collision_callback=*,gFilter=*)

    cpdef compute_collision_list(self,s,collision_callback=*,gFilter=*)

#    @cython.locals(x=cython.int,y=cython.int)
#    cpdef compute_collision_with_point(self,x,y,gFilter=*)

    cpdef get_all_sprites_on_tile(self,i,j)
