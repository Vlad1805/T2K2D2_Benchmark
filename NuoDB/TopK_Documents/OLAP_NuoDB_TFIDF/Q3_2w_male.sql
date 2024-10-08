with
    q_docLen as (
            select distinct f.id_document, sum(f.count) docLen
                from document_facts f 
                    inner join author_dimension ad on ad.id_author = f.id_author
                    inner join location_dimension ld on ld.id_location = f.id_location
                where gender='male'
                    and ld.x between 20 and 40
                    and ld.y between -100 and 100
                group by f.id_document
            ),
    q_noDocWords as (
            select f.id_word, count(distinct f.id_document) noDocWords 
                from document_facts f
                    inner join author_dimension ad on ad.id_author = f.id_author
                    inner join location_dimension ld on ld.id_location = f.id_location
                where gender='male'
                    and ld.x between 20 and 40
                    and ld.y between -100 and 100
                group by f.id_word
            )
select f.id_document,
                sum((1+(select count(id_document) from q_docLen)/ndw.noDocWords) 
                    * f.tf) TFIDF
            from 
                document_facts f
                inner join word_dimension wd on wd.id_word = f.id_word
                inner join author_dimension ad on ad.id_author = f.id_author
                inner join location_dimension ld on ld.id_location = f.id_location
                inner join q_noDocWords ndw on ndw.id_word = f.id_word
            where
                ad.gender = 'male'
                and ld.x between 20 and 40
                and ld.y between -100 and 100
                and word in ('think', 'today')
            group by f.id_document
            order by 2 desc, 1
            limit 10;
