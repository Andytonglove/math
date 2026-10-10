"""Exact F2 algebra check of a finite transformation monoid and scoped bounds.

Finite dimensionality, not 'group' alone, prevents ab=1 !=ba in finite
monoid algebras. The universal fact is proved in an accompanying math note;
this script exhausts ONE 4-element monoid only, not the universal theorem.
"""
from __future__ import annotations
import json

# All self-maps of {0,1}, sorted lexicographically; multiplication is f o g.
MAPS = tuple((a,b) for a in range(2) for b in range(2))
IDENTITY = MAPS.index((0,1))


def compose(f:tuple[int,int],g:tuple[int,int])->tuple[int,int]:
    return f[g[0]],f[g[1]]


def multiply_masks(x:int,y:int)->int:
    if not (0<=x<16 and 0<=y<16):
        raise ValueError('F2[T_2] elements are 4-bit masks')
    output=0
    for i in range(4):
        if x>>i & 1:
            for j in range(4):
                if y>>j & 1:
                    k=MAPS.index(compose(MAPS[i],MAPS[j]))
                    output ^= 1<<k
    return output


def enumerate_one_sided_inverse_pairs()->dict:
    unit=1<<IDENTITY
    pairs=[]
    for a in range(16):
        for b in range(16):
            if multiply_masks(a,b)==unit:
                pairs.append({'a_mask':a,'b_mask':b,'reverse_is_identity':multiply_masks(b,a)==unit})
    return {'carrier':'full transformation monoid on a 2-element set',
            'base_field':'F2','monoid_size':4,'algebra_size':16,
            'ordered_pairs_examined':16*16,'one_sided_inverse_pairs':pairs,
            'all_two_sided':all(x['reverse_is_identity'] for x in pairs),
            'scope':'finite one-monoid enumeration only, NOT universal proof'}


def transfer_boundary_cards()->list[dict]:
    """Human-authored epistemic gold, NOT blinded automatic evaluation."""
    return [
      {'case':'source_group_witness','question':'Does the 197 manuscript establish a particular exotic GROUP algebra witness to this evaluator?',
       'expected':'UNKNOWN','evidence':'The advanced source construction and Lean semantics have not been independently audited.',
       'logic':'epistemic, not a negation of an existence theorem'},
      {'case':'finite_dim_algebra','question':'Can a finite-dimensional unital algebra over a field contain ab=1 but ba!=1?',
       'expected':'NO','evidence':'L_a o L_b=I on the finite-dimensional vector space; hence L_b is bijective, and L_b o L_a=I, implying ba=1.',
       'logic':'universal linear algebra proof'},
      {'case':'infinite_bicyclic_monoid','question':'Can an infinite MONOID algebra have ab=1 and ba!=1?',
       'expected':'YES','evidence':'Transformations L(n)=max(n-1,0), R(n)=n+1 satisfy L o R=Id but R o L !=Id.',
       'logic':'explicit exact symbolic witness'},
      {'case':'no_inverse_hypothesis','question':'Does the right-neighbor operator identity itself imply T_b injective for arbitrary b?',
       'expected':'NO','evidence':'Take b=0 in any nontrivial group algebra: T_b=0 on a nonzero configuration space.',
       'logic':'explicit counterexample'},
      {'case':'all_fields_are_finite','question':'Does the operator algebra identity require K to be finite?',
       'expected':'NO','evidence':'Each coefficient sum is finite; any field suffices. Finite K is used for the finite alphabet interpretation.',
       'logic':'direct proof obligation scope'},
      {'case':'group_to_monoid_advanced','question':'Does a monoid one-sided inverse certify the original group algebra conjecture counterexample?',
       'expected':'NO','evidence':'A monoid need not be a group; the transformation monoid includes non-bijective L.',
       'logic':'type/domain mismatch'}
    ]


def main()->None:
    data={'enumeration':enumerate_one_sided_inverse_pairs(),
          'boundary_cards':transfer_boundary_cards()}
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
