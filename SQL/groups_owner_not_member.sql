--Find groups where owner is not a member
--These groups were made prior to update that made owners automatically members upon group creation
SELECT g.name as 'Groups where owner is not a member', g.id, g.owner_id
FROM resumes_privategroup as g
LEFT JOIN resumes_userprivategroupmembership as u
ON g.id = u.group_id AND g.owner_id = u.user_id
WHERE u.user_id IS NULL