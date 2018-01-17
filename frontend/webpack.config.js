const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const paths = {
    DIST: path.resolve(__dirname, 'dist'),
    SRC: path.resolve(__dirname, 'src'),
    JS: path.resolve(__dirname, 'src/js'),
    PUBLIC: path.resolve(__dirname, 'public'),
};

// Webpack configuration
module.exports = {
    devtool: 'inline-source-map',
    entry: './src/js/index.js',
    output: {
        path: paths.DIST,
        filename: 'index_bundle.js',
    },
    // Tell webpack to use HTML plugin
    plugins: [
        new HtmlWebpackPlugin({
            template: path.join(paths.PUBLIC, 'index.html'),
            filename: 'index.html',
            inject: 'body'
        }),
        new ExtractTextPlugin('style.bundle.css'),
    ],
    // Loaders configuration
    // We are telling webpack to use 'babel-loader' for .js and .jsx files
    module: {
         loaders: [
            { test: /\.js$/, loader: "jsx-loader" },
            { test: /\.less$/, loader: "style!css!less" }
        ],
        rules: [
            {
            test: /\.less$/,
            use: [{
                loader: "style-loader" // creates style nodes from JS strings
            }, {
                loader: "css-loader" // translates CSS into CommonJS
            }, {
                loader: "less-loader" // compiles Less to CSS
            }]
            },
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ['babel-loader'],
            }, {
                test: /\.css$/,
                loader: ExtractTextPlugin.extract({
                    use: 'css-loader',
                }),
            }, {
                test: /\.scss$/,
                loader: ExtractTextPlugin.extract({
                    use: ['css-loader', 'sass-loader'],
                }),
            }, {
                test: /\.(png|jpg|gif)$/,
                use: ['file-loader'],
            },
        ],
    },
    resolve: {
        extensions: ['.js', '.jsx'],
    },
};
