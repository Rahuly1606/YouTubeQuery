'use client';

import { useState } from 'react';
import { PlayIcon, MagnifyingGlassIcon, Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';
import { motion, AnimatePresence } from 'framer-motion';

export default function Navbar() {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    const navigation = [
        { name: 'Home', href: '/' },
        { name: 'Search', href: '#search' },
        { name: 'About', href: '#about' },
        { name: 'How It Works', href: '#how-it-works' },
    ];

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 dark:bg-gray-900/95 backdrop-blur-sm shadow-md">
            <div className="container mx-auto px-4">
                <div className="flex items-center justify-between h-16">
                    {/* Logo */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="flex items-center space-x-2"
                    >
                        <div className="relative">
                            <PlayIcon className="w-8 h-8 text-red-600" />
                            <MagnifyingGlassIcon className="w-4 h-4 text-red-500 absolute -bottom-1 -right-1" />
                        </div>
                        <span className="text-2xl font-bold bg-gradient-to-r from-red-600 to-red-500 bg-clip-text text-transparent">
                            QueryTube
                        </span>
                    </motion.div>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center space-x-8">
                        {navigation.map((item, index) => (
                            <motion.a
                                key={item.name}
                                href={item.href}
                                initial={{ opacity: 0, y: -10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className="text-gray-700 dark:text-gray-200 hover:text-red-600 dark:hover:text-red-500 
                         font-medium transition-colors duration-200"
                            >
                                {item.name}
                            </motion.a>
                        ))}
                    </div>

                    {/* Desktop CTA Buttons */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="hidden md:flex items-center space-x-4"
                    >
                        <a
                            href="https://github.com/yourusername/querytube"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-gray-700 dark:text-gray-200 hover:text-red-600 dark:hover:text-red-500 
                       font-medium transition-colors duration-200"
                        >
                            GitHub
                        </a>
                        <button className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg 
                             font-medium transition-colors duration-200 shadow-lg hover:shadow-xl">
                            Get Started
                        </button>
                    </motion.div>

                    {/* Mobile Menu Button */}
                    <button
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        className="md:hidden text-gray-700 dark:text-gray-200 p-2"
                    >
                        {mobileMenuOpen ? (
                            <XMarkIcon className="w-6 h-6" />
                        ) : (
                            <Bars3Icon className="w-6 h-6" />
                        )}
                    </button>
                </div>
            </div>

            {/* Mobile Menu */}
            <AnimatePresence>
                {mobileMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.2 }}
                        className="md:hidden bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700"
                    >
                        <div className="container mx-auto px-4 py-4 space-y-3">
                            {navigation.map((item) => (
                                <a
                                    key={item.name}
                                    href={item.href}
                                    onClick={() => setMobileMenuOpen(false)}
                                    className="block text-gray-700 dark:text-gray-200 hover:text-red-600 dark:hover:text-red-500 
                           font-medium py-2 transition-colors duration-200"
                                >
                                    {item.name}
                                </a>
                            ))}
                            <div className="pt-3 space-y-2">
                                <a
                                    href="https://github.com/yourusername/querytube"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="block text-gray-700 dark:text-gray-200 hover:text-red-600 dark:hover:text-red-500 
                           font-medium py-2 transition-colors duration-200"
                                >
                                    GitHub
                                </a>
                                <button className="w-full bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg 
                                 font-medium transition-colors duration-200 shadow-lg">
                                    Get Started
                                </button>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </nav>
    );
}
