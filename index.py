import VectorFilter as Vf

vectorFilter = Vf.VectorFilter()

row = "59449/55318\">PDF (Українська)</a></div><div><h4>References</h4><br><div><p>Tikhonov А.N., Аrsenin V.YA. Metody resheniya nekorrektnykh zadach. — M.: Nauka, 1979. — 284 s.</p><p></p><p>Forsayt Dzh., Mal’kol’m M., Mouler K. Mashinnyye metody matematicheskikh vychisleniy: Per. s angl. Ikramova KH.D. — M.: Mir, 1980. — 277 s.</p><p></p><p>Gutenmakher L.I., Timoshenko YU.А., Tikhonchuk S.T. O dinamicheskom metode resheniya nekorrektnykh zadach // Dokl. АN SSSR. — 1977. — 237. — № 4. — S. 776–778.</p><p></p><p>Vasil’yeva А.B., Tikhonov А.N. Integral’nyye uravneniya. — M: Fizmatlit, 2002. — 158 s.</p><p></p></div><br"
vectorFilter.parse_row(row)
print(vectorFilter.to_array())
