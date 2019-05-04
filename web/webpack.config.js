const devMode = process.env.NODE_ENV !== 'production';

const path = require('path');
const webpack = require('webpack');
const CleanPlugin = require('clean-webpack-plugin');
const ManifestPlugin = require('webpack-manifest-plugin');

const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const CssNano = require('cssnano');
const TerserPlugin = require('terser-webpack-plugin');
const CompressionPlugin = require('compression-webpack-plugin');

const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
    entry: {
        index: 'index.js',
		login: 'login.js',
		register: 'register.js',
		allitems: 'allitems.js',
		cart: 'cart.js',
		item: 'item.js',
    },
    output: {
        path: path.join(__dirname, 'public', 'components'),
        publicPath: '/components/',
        filename: devMode ? '[name].js' : '[name]-[chunkhash].js',
    },
    optimization: {
        minimizer: [
            new TerserPlugin({
                cache: true,
                parallel: true,
                sourceMap: true,
                terserOptions: {
                    compress: true,
                    ecma: 6,
                    output: {
                        comments: false,
                        beautify: false,
                    }
                },
            }),
            new OptimizeCSSAssetsPlugin({
                cssProcesor: CssNano,
                cssProcessorOptions: {
                    discardComemnts: {
                        removeAll: true,
                    },
                    safe: true,
                },
            })
        ]
    },
    resolve: {
        modules: [path.resolve(__dirname, 'components'), path.resolve(__dirname, 'node_modules')],
        extensions: ['.js', '.es6', '.css', '.sass', '.scss', '.vue'],
    },
    plugins: [
        new CleanPlugin(['public/components/']),
        new CompressionPlugin(),
        new ManifestPlugin({
            writeToFileEmit: true,
            publicPath: '/public/components/',
        }),
        new VueLoaderPlugin(),
    ],
    module: {
        rules: [
            {
                test: /\.(sass|scss|css)$/,
                use: [
                    'style-loader',
                    'vue-style-loader',
                    'css-loader',
                    'postcss-loader',
                    'sass-loader',
                ]
            },
            {
                test: /\.(jpe?g|png|gif)$/i,
                use: {
                    loader: 'url-loader',
                    options: {
                        limit: 8192
                    },
                },
            },
            {
                test: /\.woff($|\?)|\.woff2($|\?)|\.tff($|\?)|\.eot($|\?)|\.svg($|\?)/,
                use: {
                    loader: 'url-loader',
                    options: {
                        limit: 10000
                    },
                },
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
						plugins: ['@babel/plugin-transform-runtime'],
                    }
                }
            },
        ]
    }
};
