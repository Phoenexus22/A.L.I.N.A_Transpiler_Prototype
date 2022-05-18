<h1>A.L.I.N.A. Transpiler Prototype</h1>
<h2>at least it's not assembly</h2>
<p>this is the c transpiler for a programming language with structural simmilarities to assembly, but with features of higher level languages</p>
<p> the basic structure of a line in Alina is as follows: label(optional)>(optional)instruction:value1, value2(optional), value3(optional) (...);</p>
<br>
<p>!WARNING! the language is still under development, functionality may change over time</p>
<br>
<h2>Instructions:</h2>
<table>
  <tr><th>Instruction</th><th>No. of values</th><th>Value Structure</th><th>Function</th></tr>
  <tr><td>set</td><td>2</td><td>(Memory Address),(Value to Set)</td><td>changes the value at a memory location to the value specified</td></tr>
  <tr><td>mset</td><td>Var</td><td>(First Memory Address),(Value1 to Set),(Value2 to Set)(opt),(...)</td><td>changes the value of multiple consecutive memory cells to the corresponding value</td></tr>
  <tr><td>cpy</td><td>3</td><td>(Memory Address Source),(Memory Address Copy),(Length)</td><td>copies multiple values from consecutive memory cells to elswhere in the memory</td></tr>
</table>
