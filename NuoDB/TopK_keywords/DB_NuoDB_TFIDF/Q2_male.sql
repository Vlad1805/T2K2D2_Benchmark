with 
        q_wordCountDocs as (select v.id_word as id_word, count(distinct v.id_document) as wordCountDocs
                                from vocabulary v 
                                where v.id_document in (select d.id
                                                        from documents d
                                                        inner join (documents_authors da
                                                            inner join (authors a
                                                                inner join (genders g)
                                                                on a.id_gender = g.id)
                                                            on da.id_author = a.id)
                                                        on d.id = da.id_document
                                                        where g.type = 'male'
                                                            and d.document_date between '2015-09-17 00:00:00' and '2015-09-18 00:00:00')
                                group by v.id_word
                        ),
        q_noDocs as (select d.id as id
                        from documents d
                            inner join (documents_authors da
                                inner join (authors a
                                    inner join (genders g)
                                    on a.id_gender = g.id)
                                on da.id_author = a.id)
                            on d.id = da.id_document
                        where g.type = 'male'                          
                            and d.document_date between '2015-09-17 00:00:00' and '2015-09-18 00:00:00')

    select q2.word as word, sum(q2.tfidf) as stfidf 
        from
            (select d.id as id, w.word as word, -- v.id_word, v.tf, q_dl.docLen, q_wcd.wordCountDocs,
                  v.tf * (1 + (select count(id) from q_noDocs)/q_wcd.wordCountDocs) as tfidf
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
                inner join (q_wordCountDocs q_wcd)
                on q_wcd.id_word =  v.id_word
            where g.type = 'male'
                and d.document_date between '2015-09-17 00:00:00' and '2015-09-18 00:00:00') q2
        group by word
        order by 2 desc
        limit 10;
