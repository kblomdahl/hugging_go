from hugging_go.sgf import parse_sgf_sequence
from hugging_go.vertex import Vertex

import unittest

class TestSgf(unittest.TestCase):
    def test_bad_sgf(self):
        self.assertEqual(
            parse_sgf_sequence(';B[zz];W[aa]'),
            []
        )

    def test_small(self):
        self.assertEqual(
            parse_sgf_sequence(';B[dd];W[aa];B[tt]'),
            ['d4', 'a1', 'pass']
        )

    def test_example(self):
        sgf = '(;GM[1]FF[4]SZ[19]GN[]DT[2021-05-28]PB[kizuna20]PW[amaru15]BR[9æ®µ]WR[9æ®µ]KM[0]HA[0]RU[Japanese]AP[GNU Go:3.8]RE[W+0.02]TM[60]TC[3]TT[15]AP[foxwq]RL[0];B[pd];W[dp];B[pp];W[dc];B[ce];W[cd];B[de];W[fc];B[di];W[qq];B[qp];W[pq];B[nq];W[oq];B[op];W[nr];B[rq];W[rr];B[or];W[rp];B[qr];W[sq];B[pr];W[rq];B[mr];W[np];B[mq];W[oo];B[no];W[mp];B[on];W[qn];B[po];W[lp];B[kq];W[pl];B[ln];W[fq];B[cn];W[qf];B[nc];W[qd];B[qc];W[rc];B[qe];W[rd];B[pf];W[re];B[pe];W[qg];B[cp];W[cq];B[bq];W[co];B[bp];W[dn];B[bo];W[do];B[dm];W[iq];B[kp];W[dj];B[em];W[ci];B[ch];W[bh];B[dh];W[bj];B[ej];W[dk];B[ek];W[bg];B[dq];W[cr];B[dr];W[er];B[br];W[eq];B[cs];W[fo];B[be];W[ic];B[bl];W[bk];B[ck];W[cl];B[dl];W[cj];B[bm];W[ai];B[ed];W[ec];B[jc];W[jb];B[kb];W[ib];B[qb];W[pi];B[kc];W[ie];B[hf];W[if];B[ig];W[hg];B[gf];W[hh];B[fh];W[ji];B[jg];W[hj];B[oi];W[pj];B[hp];W[ip];B[hn];W[io];B[ok];W[oj];B[nj];W[nk];B[pm];W[qm];B[ol];W[pk];B[mj];W[jm];B[hl];W[lm];B[jk];W[kk];B[ag];W[ak];B[kj];W[jj];B[kl];W[lk];B[jl];W[lj];B[ki];W[kh];B[li];W[mk];B[mh];W[mg];B[lh];W[kg];B[nh];W[ni];B[mi];W[nm];B[jf];W[lf];B[af];W[ah];B[lg];W[og];B[ng];W[le];B[kf];W[jh])'
        sequence = parse_sgf_sequence(sgf)

        self.assertEqual(len(sequence), 160)

if __name__ == '__main__':
    unittest.main()
