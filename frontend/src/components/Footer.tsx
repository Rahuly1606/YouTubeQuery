'use client';

import { PlayIcon, MagnifyingGlassIcon, HeartIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';

export default function Footer() {
    const currentYear = new Date().getFullYear();

    const quickLinks = [
        { name: 'GitHub', href: 'https://github.com/Rahuly1606/YouTubeQuery' },
        { name: 'Docs', href: '/api/docs' },
        { name: 'About', href: '#about' },
        { name: 'Contact', href: '#contact' },
    ];

    return (
        <footer className="bg-gray-900 text-gray-300">
            <div className="container mx-auto px-4 py-8">
                {/* Main Content */}
                <div className="flex flex-col md:flex-row justify-between items-center gap-6 mb-6">
                    {/* Brand */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="flex items-center space-x-2"
                    >
                        <div className="relative">
                            <PlayIcon className="w-6 h-6 text-red-600" />
                            <MagnifyingGlassIcon className="w-3 h-3 text-red-500 absolute -bottom-0.5 -right-0.5" />
                        </div>
                        <span className="text-xl font-bold text-white">QueryTube</span>
                    </motion.div>

                    {/* Quick Links */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.1 }}
                        className="flex flex-wrap justify-center gap-6"
                    >
                        {quickLinks.map((link) => (
                            <a
                                key={link.name}
                                href={link.href}
                                target={link.href.startsWith('http') ? '_blank' : undefined}
                                rel={link.href.startsWith('http') ? 'noopener noreferrer' : undefined}
                                className="text-gray-400 hover:text-red-500 transition-colors duration-200"
                            >
                                {link.name}
                            </a>
                        ))}
                    </motion.div>

                    {/* Social Icons */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.2 }}
                        className="flex items-center space-x-4"
                    >
                        <a
                            href="https://github.com/Rahuly1606/YouTubeQuery"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-xl hover:text-red-500 transition-colors duration-200"
                            aria-label="GitHub"
                        >
                            ⚡
                        </a>
                        <a
                            href="https://twitter.com/querytube"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-xl hover:text-red-500 transition-colors duration-200"
                            aria-label="Twitter"
                        >
                            𝕏
                        </a>
                    </motion.div>
                </div>

                {/* Divider */}
                <div className="border-t border-gray-800 my-4"></div>

                {/* Bottom Section */}
                <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-gray-400">
                    <motion.div
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                        className="flex items-center space-x-1"
                    >
                        <span>© {currentYear} QueryTube</span>
                        <span>•</span>
                        <span className="flex items-center">
                            Made with <HeartIcon className="w-3 h-3 mx-1 text-red-500 fill-red-500 animate-pulse" /> by developers
                        </span>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                        className="text-gray-500 text-xs"
                    >
                        Powered by <span className="text-red-500 font-semibold">FastAPI</span> • <span className="text-red-500 font-semibold">Next.js</span> • <span className="text-red-500 font-semibold">FAISS</span>
                    </motion.div>
                </div>
            </div>
        </footer>
    );
}
