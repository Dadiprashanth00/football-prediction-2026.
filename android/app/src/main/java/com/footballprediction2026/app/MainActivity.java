package com.footballprediction2026.app;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import androidx.activity.OnBackPressedCallback;
import androidx.appcompat.app.AppCompatActivity;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;
import androidx.webkit.WebViewAssetLoader;

/**
 * Football Prediction 2026 – Android shell.
 * The whole app (dashboard + prediction engine) ships inside assets/www, so it
 * works offline in demo mode; live providers are called over HTTPS when an API
 * key is configured in the in-app settings.
 */
public class MainActivity extends AppCompatActivity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final String START = "https://" + HOST + "/assets/www/index.html";
    private WebView web;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.parseColor("#05150f"));
        getWindow().setNavigationBarColor(Color.parseColor("#05150f"));

        SwipeRefreshLayout swipe = new SwipeRefreshLayout(this);
        web = new WebView(this);
        web.setBackgroundColor(Color.parseColor("#071d16"));
        swipe.addView(web);
        swipe.setColorSchemeColors(Color.parseColor("#ffd23f"));
        swipe.setProgressBackgroundColorSchemeColor(Color.parseColor("#0f3126"));
        swipe.setOnRefreshListener(() -> {
            web.evaluateJavascript("document.getElementById('refreshBtn').click()", null);
            swipe.postDelayed(() -> swipe.setRefreshing(false), 1200);
        });
        // only allow pull-to-refresh when the page is scrolled to the top
        web.getViewTreeObserver().addOnScrollChangedListener(() -> swipe.setEnabled(web.getScrollY() == 0));
        setContentView(swipe);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);          // localStorage for settings / cache
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);
        s.setMediaPlaybackRequiresUserGesture(true);
        s.setTextZoom(100);

        final WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
                .setDomain(HOST)
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();

        web.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                return loader.shouldInterceptRequest(request.getUrl());
            }
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri u = request.getUrl();
                if (HOST.equals(u.getHost())) return false;
                // external links (provider sign-up pages etc.) open in the browser
                startActivity(new Intent(Intent.ACTION_VIEW, u));
                return true;
            }
        });

        getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                // close an open match sheet / dialog first, then exit
                web.evaluateJavascript(
                    "(function(){var s=document.getElementById('sheet'),d=document.getElementById('dlg');" +
                    "if(s&&s.classList.contains('on')||d&&d.classList.contains('on')){" +
                    "document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}));return 1}return 0})()",
                    v -> { if (!"1".equals(v)) finish(); });
            }
        });

        if (savedInstanceState != null) web.restoreState(savedInstanceState);
        else web.loadUrl(START);
    }

    @Override
    protected void onSaveInstanceState(Bundle out) {
        super.onSaveInstanceState(out);
        web.saveState(out);
    }
}
