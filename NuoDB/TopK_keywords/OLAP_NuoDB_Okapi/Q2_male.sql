-- top-K keywords Okapi by gender : date  -- OK
with
    q_docLen as (
            select distinct id_document, sum(count) docLen
                from document_facts f 
                    inner join author_dimension ad on ad.id_author = f.id_author
                    inner join time_dimension td on td.id_time = f.id_time
                where gender='male'
                    and td.full_date between '2015-09-17 00:00:00' and '2015-09-18 00:00:00'
                group by f.id_document
                )
select wd.word, 
                (1+(select count(id_document) from q_docLen)/count(distinct f.id_document)) 
                    * (1.6 + 1) * 
                    sum(f.tf/(f.tf + 1.6*(1-0.75+
                        0.75*dl.docLen/
                            (select avg(docLen) from q_docLen)
                        ))) Okapi          
            from 
                document_facts f
                inner join author_dimension ad on ad.id_author = f.id_author
                inner join word_dimension wd on wd.id_word = f.id_word
                inner join time_dimension td on td.id_time = f.id_time
                inner join q_docLen dl on dl.id_document = f.id_document
            where
                ad.gender = 'male'
                and td.full_date between '2015-09-17 00:00:00' and '2015-09-18 00:00:00'
            group by wd.word
            order by 2 desc
            limit 10;
            