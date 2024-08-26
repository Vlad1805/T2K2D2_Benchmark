-- top-K keywords TFIDF by gender & location - ok
with
    noDocs as (select distinct id_document 
                from document_facts f 
                    inner join author_dimension ad on ad.id_author = f.id_author
                    inner join location_dimension ld on ld.id_location = f.id_location
                where ad.gender='female'
                    and ld.x between 20 and 40
                    and ld.y between -100 and 100
                )
    select wd.word, sum(f.tf) * (1+(select count(id_document) from noDocs)/count(distinct f.id_document)) TFIDF
    from 
        document_facts f
        inner join author_dimension ad on ad.id_author = f.id_author
        inner join word_dimension wd on wd.id_word = f.id_word
        inner join location_dimension ld on ld.id_location = f.id_location
    where
        ad.gender = 'female'
        and ld.x between 20 and 40
        and ld.y between -100 and 100
    group by wd.word
    order by 2 desc
    limit 10;
