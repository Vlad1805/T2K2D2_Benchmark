with 
        q_wordCountDocs as (select v.id_word id_word, count(distinct v.id_document) wordCountDocs
                                from vocabulary v 
                                where v.id_document in (select d.id
                                                        from documents d
                                                        inner join (documents_authors da
                                                            inner join (authors a
                                                                inner join (genders g)
                                                                on a.id_gender = g.id)
                                                            on da.id_author = a.id)
                                                        on d.id = da.id_document
                                                        inner join geo_location gl
                                                            on d.id_geo_loc = gl.id 
                                                        where g.type = 'male'
                                                            and gl.X between 20 and 40
                                                            and gl.Y between -100 and 100)
                                group by v.id_word
                        ),
        q_noDocs as (select d.id id
                        from documents d
                            inner join (documents_authors da
                                inner join (authors a
                                    inner join (genders g)
                                    on a.id_gender = g.id)
                                on da.id_author = a.id)
                            on d.id = da.id_document
                            inner join geo_location gl
                            on d.id_geo_loc = gl.id 
                        where g.type = 'male'
                            and gl.X between 20 and 40
                            and gl.Y between -100 and 100)
select q2.id, sum(q2.tfidf) stfidf 
        from
            (select d.id id, w.word word,
                  (v.tf * (1 + (select count(id) from q_noDocs )/q_wcd.wordCountDocs)) tfidf
            from documents d
                inner join (vocabulary v
                    inner join (words w) 
                    on w.id = v.id_word)
                on v.id_document = d.id
                inner join (documents_authors da
                    inner join (authors a
                        inner join (genders g)
                        on a.id_gender = g.id)
                    on da.id_author = a.id)
                on d.id = da.id_document
                inner join geo_location gl
                on d.id_geo_loc = gl.id 
                inner join q_wordCountDocs q_wcd
                on q_wcd.id_word =  v.id_word
            where g.type = 'male'
                and gl.X between 20 and 40
                and gl.Y between -100 and 100
                and w.word in ('think', 'today')) q2
            group by q2.id
            order by 2 desc, 1
            limit 10;
