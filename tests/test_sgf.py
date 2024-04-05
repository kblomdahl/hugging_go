from hugging_go.sgf import parse_sgf
from hugging_go.vertex import Vertex

import unittest

class TestSgf(unittest.TestCase):
    def test_bad_sgf(self):
        self.assertEqual(
            parse_sgf(';B[zz];W[aa]').sequence,
            []
        )

    def test_small(self):
        self.assertEqual(
            parse_sgf(';B[dd];W[aa];B[tt]').sequence,
            ['Bd4', 'Wa1', 'Bpass']
        )

    def test_example(self):
        text = '(;GM[1]FF[4]SZ[19]GN[]DT[2021-05-28]PB[kizuna20]PW[amaru15]BR[9æ®µ]WR[9æ®µ]KM[0]HA[0]RU[Japanese]AP[GNU Go:3.8]RE[W+0.02]TM[60]TC[3]TT[15]AP[foxwq]RL[0];B[pd];W[dp];B[pp];W[dc];B[ce];W[cd];B[de];W[fc];B[di];W[qq];B[qp];W[pq];B[nq];W[oq];B[op];W[nr];B[rq];W[rr];B[or];W[rp];B[qr];W[sq];B[pr];W[rq];B[mr];W[np];B[mq];W[oo];B[no];W[mp];B[on];W[qn];B[po];W[lp];B[kq];W[pl];B[ln];W[fq];B[cn];W[qf];B[nc];W[qd];B[qc];W[rc];B[qe];W[rd];B[pf];W[re];B[pe];W[qg];B[cp];W[cq];B[bq];W[co];B[bp];W[dn];B[bo];W[do];B[dm];W[iq];B[kp];W[dj];B[em];W[ci];B[ch];W[bh];B[dh];W[bj];B[ej];W[dk];B[ek];W[bg];B[dq];W[cr];B[dr];W[er];B[br];W[eq];B[cs];W[fo];B[be];W[ic];B[bl];W[bk];B[ck];W[cl];B[dl];W[cj];B[bm];W[ai];B[ed];W[ec];B[jc];W[jb];B[kb];W[ib];B[qb];W[pi];B[kc];W[ie];B[hf];W[if];B[ig];W[hg];B[gf];W[hh];B[fh];W[ji];B[jg];W[hj];B[oi];W[pj];B[hp];W[ip];B[hn];W[io];B[ok];W[oj];B[nj];W[nk];B[pm];W[qm];B[ol];W[pk];B[mj];W[jm];B[hl];W[lm];B[jk];W[kk];B[ag];W[ak];B[kj];W[jj];B[kl];W[lk];B[jl];W[lj];B[ki];W[kh];B[li];W[mk];B[mh];W[mg];B[lh];W[kg];B[nh];W[ni];B[mi];W[nm];B[jf];W[lf];B[af];W[ah];B[lg];W[og];B[ng];W[le];B[kf];W[jh])'
        sgf = parse_sgf(text)

        self.assertEqual(sgf.success, True)
        self.assertEqual(sgf.winner, 'W')
        self.assertEqual(sgf.komi, 0)
        self.assertEqual(len(sgf.sequence), 160)

    def test_empty_vertex(self):
        text = '(;GM[1]FF[4]SZ[19]PW[glad]WR[4d]PB[ChouNewbie]BR[4d]DT[2007-05-28]PC[The KGS Go Server at http://www.gokgs.com/]KM[6.50]RE[W+18.50]RU[Japanese]CA[UTF-8]ST[2]AP[CGoban:3]TM[180]OT[5x20 byo-yomi];B[pd];W[dp];B[oo];W[dd];B[dm];W[fm];B[dj];W[pp];B[po];W[qp];B[qo];W[nq];B[mp];W[np];B[no];W[mo];B[kp];W[mn];B[mq];W[rp];B[nr];W[or];B[mr];W[ro];B[qm];W[qk];B[nm];W[kn];B[pr];W[pq];B[os];W[qr];B[oq];W[op];B[nk];W[rm];B[rl];W[ql];B[rn];W[pm];B[sm];W[nn];B[rk];W[on];B[qn];W[rj];B[qj];W[ri];B[qh];W[rh];B[qg];W[rg];B[qi];W[qf];B[pl];W[pk];B[ol];W[oj];B[pf];W[pg];B[qe];W[rf];B[og];W[nj];B[mj];W[ph];B[mi];W[pi];B[sk];W[so];B[sn];W[of];B[pe];W[nf];B[mc];W[pc];B[oc];W[qc];B[nd];W[jq];B[jo];W[ml];B[hp];W[hq];B[gp];W[gq];B[rr];W[or];B[fp];W[fq];B[qs];W[ps];B[ok];W[pj];B[pr];W[oe];B[qq];W[od];B[mk];W[ll];B[mf];W[ob];B[jk];W[im];B[hk];W[io];B[ip];W[jp];B[ko];W[kq];B[in];W[lp];B[lo];W[jn];B[ho];W[lq];B[hm];W[rq];B[qr];W[ns];B[oq];W[ln];B[io];W[or];B[ms];W[lr];B[oq];W[il];B[hl];W[or];B[ns];W[ls];B[oq];W[ik];B[or];W[ij];B[gi];W[nc];B[ih];W[jh];B[ji];W[ii];B[jg];W[kh];B[ki];W[hh];B[ig];W[hi];B[lh];W[dn];B[iq];W[ir];B[hr];W[jr];B[eq];W[gr];B[fr];W[hs];B[ep];W[dq];B[en];W[cn];B[em];W[er];B[gj];W[hg];B[ie];W[eh];B[ch];W[dg];B[bf];W[ce];B[cm];W[ge];B[hc];W[mb];B[eb];W[fc];B[fb];W[gc];B[gb];W[hd];B[ic];W[lc];B[id];W[cb];B[be];W[bd];B[bn];W[bo];B[bm];W[ej];B[dk];W[di];B[ci];W[eo];B[fn];W[fo];B[gn];W[do];B[ao];W[ap];B[an];W[bq];B[ek];W[kf];B[kg];W[cf];B[cg];W[lf];B[mg];W[me];B[kb];W[kc];B[jc];W[fh];B[gh];W[gg];B[fj];W[ae];B[bg];W[kk];B[jj];W[jl];B[dh];W[ei];B[eg];W[fg];B[df];W[ee];B[ef];W[ff];B[ec];W[ed];B[he];W[gd];B[lb];W[md];B[kd];W[la];B[jb];W[ld];B[db];W[ca];B[af];W[ad];B[dc];W[cc];B[ng];W[da];B[ke];W[go];B[hn];W[le];B[jf];W[ea];B[ka];W[fa];B[hb];W[ma];B[lk];W[kj];B[lj];W[kl];B[hf];W[nh];B[gf];W[mh];B[fe];W[fd];B[lg];W[om];B[nl];W[ni];B[mm];W[lm];B[li];W[oh];B[ga];W[sj];B[dg];W[de];B[];W[])'
        sgf = parse_sgf(text)

        self.assertEqual(sgf.success, True)
        self.assertEqual(sgf.winner, 'W')
        self.assertEqual(sgf.komi, 6.5)
        self.assertEqual(sgf.sequence[:2], ['Bq4', 'Wd16'])
        self.assertEqual(len(sgf.sequence), 284)

    def test_handicap(self):
        text = '(;GM[1]FF[4]SZ[19]PW[gorillazz]WR[4d]PB[pwanda]BR[2d]DT[2007-07-02]PC[The KGS Go Server at http://www.gokgs.com/]KM[0.50]RE[W+Resign]RU[Japanese]OT[5x15 byo-yomi]CA[UTF-8]ST[2]AP[CGoban:3]TM[60]HA[2]AB[pd][dp];W[dd];B[pp];W[nc];B[jd];W[qc];B[pc];W[qd];B[pe];W[pb];B[ob];W[qb];B[oc];W[qf];B[nd];W[cn];B[dk];W[en];B[fp];W[di];B[co];W[bn];B[bo];W[fm];B[fk];W[hm];B[ei];W[eh];B[fi];W[dj];B[ek];W[dg];B[dm];W[dn];B[hp];W[ii];B[fh];W[ie];B[ff];W[id];B[fd];W[jc];B[df];W[cf];B[eg];W[dh];B[de];W[ce];B[ed];W[dc];B[ik];W[gg];B[fg];W[hk];B[hj];W[ij];B[hl];W[il];B[gl];W[jk];B[gm];W[gn];B[hn];W[im];B[go];W[bk];B[ck];W[bl];B[cj];W[bi];B[ci];W[bh];B[bj];W[aj];B[fn];W[mc];B[kc];W[md];B[jb];W[ic];B[pf];W[qg];B[le];W[me];B[pg];W[lf];B[qh];W[ph];B[rh];W[rg];B[ng];W[pi];B[qj];W[pj];B[qk];W[pk];B[ne];W[mf];B[nf];W[ql];B[rl];W[qm];B[rm];W[qn];B[rn];W[qo];B[np];W[ro];B[qi];W[lp];B[lq];W[kq];B[mq];W[kp];B[rq];W[oh];B[og];W[oe];B[nh];W[nj];B[lh];W[mi];B[lg];W[kf];B[jh];W[ih];B[kj];W[li];B[ki];W[kg];B[kh];W[lk];B[kk];W[kl];B[ll];W[mk];B[km];W[jl];B[ml];W[nl];B[nm];W[om];B[ol];W[nk];B[ig];W[hg];B[hf];W[if];B[jg];W[gf];B[he];W[ge];B[hd];W[gd];B[hc];W[hb];B[hh];W[jn];B[ln];W[jo];B[iq];W[mg];B[mh];W[nb];B[oa];W[ni];B[on];W[pm];B[kr];W[jr];B[lr];W[jq];B[ir];W[js];B[is];W[jf];B[gk];W[jj];B[hi];W[qe];B[in];W[jm];B[lo];W[na];B[ko];W[jp];B[mp];W[pa];B[io];W[lj];B[ks];W[od];B[kn];W[ji])'
        sgf = parse_sgf(text)

        self.assertEqual(sgf.success, True)
        self.assertEqual(sgf.winner, 'W')
        self.assertEqual(sgf.komi, 0.5)
        self.assertEqual(sgf.sequence[:5], ['Bq4', 'Bd16', 'Wd4', 'Bq16', 'Wo3'])
        self.assertEqual(len(sgf.sequence), 195)

if __name__ == '__main__':
    unittest.main()
