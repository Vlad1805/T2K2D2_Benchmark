with
    q_docLen as (
            select distinct f.id_document, sum(f.count) docLen
                from document_facts f 
                    inner join author_dimension ad on ad.id_author = f.id_author
                    inner join time_dimension td on td.id_time = f.id_time
                where gender='female'
                    and td.full_date between '2015-09-17 00:00:00' and '2015-09-18 00:00:00'
                group by f.id_document
            ),
    q_noDocWords as (
            select f.id_word, count(distinct f.id_document) noDocWords 
                from document_facts f
                    inner join author_dimension ad on ad.id_author = f.id_author
                    inner join time_dimension td on td.id_time = f.id_time
                where gender='female'
                    and td.full_date between '2015-09-17 00:00:00' and '2015-09-18 00:00:00'
                group by f.id_word
            )
select f.id_document,
                sum((1+(select count(id_document) from q_docLen)/ndw.noDocWords) 
                    * f.tf) TFIDF
            from 
                document_facts f
                inner join word_dimension wd on wd.id_word = f.id_word
                inner join author_dimension ad on ad.id_author = f.id_author
                inner join time_dimension td on td.id_time = f.id_time
                inner join q_noDocWords ndw on ndw.id_word = f.id_word
            where
                ad.gender = 'female'
                and td.full_date between '2015-09-17 00:00:00' and '2015-09-18 00:00:00'
                and word in ('think', 'today', 'friday')
            group by f.id_document
            order by 2 desc, 1
            limit 10;
