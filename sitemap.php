<?php
/**
 * sitemap.php — TechFlair
 * Génère un sitemap XML dynamique en interrogeant Supabase REST API.
 * Soumettre à Google Search Console : https://tech-flair.com/sitemap.php
 */

header('Content-Type: application/xml; charset=utf-8');
header('Cache-Control: public, max-age=3600');

$SUPABASE_URL  = 'https://yrgylnmhqcimwgmjponj.supabase.co';
$SUPABASE_ANON = 'sb_publishable__SdwJpIWNVfPfVNX7eFc-w_mQA8av6H';
$SITE_URL      = 'https://tech-flair.com';

// Pages statiques
$static_pages = [
    ['loc' => $SITE_URL . '/',                              'priority' => '1.0', 'changefreq' => 'daily'],
    ['loc' => $SITE_URL . '/categorie.html?cat=tests',      'priority' => '0.8', 'changefreq' => 'weekly'],
    ['loc' => $SITE_URL . '/categorie.html?cat=gadgets',    'priority' => '0.8', 'changefreq' => 'weekly'],
    ['loc' => $SITE_URL . '/categorie.html?cat=logiciels',  'priority' => '0.8', 'changefreq' => 'weekly'],
    ['loc' => $SITE_URL . '/contact.html',                  'priority' => '0.4', 'changefreq' => 'monthly'],
    ['loc' => $SITE_URL . '/mentions-legales.html',         'priority' => '0.3', 'changefreq' => 'yearly'],
    ['loc' => $SITE_URL . '/confidentialite.html',          'priority' => '0.3', 'changefreq' => 'yearly'],
];

// Récupérer les articles publiés depuis Supabase
$articles = [];
$api_url = $SUPABASE_URL . '/rest/v1/articles?select=slug,date_creation,date_modification&statut=eq.publié&order=date_creation.desc';

$ch = curl_init($api_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'apikey: ' . $SUPABASE_ANON,
    'Authorization: Bearer ' . $SUPABASE_ANON,
    'Accept: application/json',
]);
curl_setopt($ch, CURLOPT_TIMEOUT, 5);
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($http_code === 200 && $response) {
    $data = json_decode($response, true);
    if (is_array($data)) {
        $articles = $data;
    }
}

// Génération du XML
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

<?php foreach ($static_pages as $page): ?>
  <url>
    <loc><?= htmlspecialchars($page['loc']) ?></loc>
    <changefreq><?= $page['changefreq'] ?></changefreq>
    <priority><?= $page['priority'] ?></priority>
  </url>
<?php endforeach; ?>

<?php foreach ($articles as $article):
    if (empty($article['slug'])) continue;
    $lastmod = !empty($article['date_modification'])
        ? date('Y-m-d', strtotime($article['date_modification']))
        : (!empty($article['date_creation']) ? date('Y-m-d', strtotime($article['date_creation'])) : date('Y-m-d'));
?>
  <url>
    <loc><?= htmlspecialchars($SITE_URL . '/article.html?slug=' . $article['slug']) ?></loc>
    <lastmod><?= $lastmod ?></lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
<?php endforeach; ?>

</urlset>
